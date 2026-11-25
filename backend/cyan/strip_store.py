from fastapi import HTTPException

from cyan.pairing import disposition

SIDES = ("short", "long")
SIDE_NAMES = {"short": "短洗", "long": "长洗"}


def _num(value):
    return None if value is None else float(value)


def _reading(row):
    if row is None:
        return None
    return {
        "id": row["id"],
        "side": row["side"],
        "temp": _num(row["temp"]),
        "density": _num(row["density"]),
        "fade": _num(row["fade"]),
        "state": row["state"],
        "received_at": row["received_at"],
    }


def _grouped(connection, code, strip=None):
    sql = "SELECT * FROM strip_readings WHERE plate=%s"
    params = [code]
    if strip is not None:
        sql += " AND strip=%s"
        params.append(strip)
    rows = connection.execute(sql + " ORDER BY strip,side,id", params).fetchall()
    grouped = {}
    for row in rows:
        grouped.setdefault((row["strip"], row["side"]), []).append(row)
    return grouped


def _active(rows):
    return [row for row in rows if row["state"] == "active"]


def _present(strip, grouped):
    out = {
        "plate": strip["plate"],
        "code": strip["code"],
        "state": strip["state"],
    }
    listed_all = []
    for side in SIDES:
        rows = grouped.get((strip["code"], side), [])
        listed = [_reading(row) for row in rows]
        listed_all.extend(listed)
        active = [row for row in listed if row["state"] == "active"]
        out[side + "_readings"] = listed
        out[side] = active[0] if len(active) == 1 else None
        out[side + "_active"] = len(active)
    short, long = out["short"], out["long"]
    out["readings"] = listed_all
    # 同侧多份读数即冲突；两份都留档，试条按隔离处理。
    out["conflict"] = any(out[side + "_active"] > 1 for side in SIDES)
    out["complete"] = short is not None and long is not None
    out["missing"] = [side for side in SIDES if out[side + "_active"] == 0]
    out["temp_gap"] = abs(short["temp"] - long["temp"]) if out["complete"] else None
    for side in SIDES:
        reading = out[side]
        out[side + "_temp"] = reading["temp"] if reading else None
        out[side + "_density"] = reading["density"] if reading else None
    out["long_fade"] = long["fade"] if long else None
    return out


def list_pairs(connection, code):
    grouped = _grouped(connection, code)
    strips = connection.execute(
        "SELECT * FROM strips WHERE plate=%s ORDER BY code", (code,)
    ).fetchall()
    return [_present(strip, grouped) for strip in strips]


def one(connection, code, strip):
    row = connection.execute(
        "SELECT * FROM strips WHERE plate=%s AND code=%s", (code, strip)
    ).fetchone()
    if row is None:
        raise HTTPException(404, "试条不存在")
    return _present(row, _grouped(connection, code, strip))


def derive_state(grouped, strip):
    """Same side with two different readings: both stay, the pair is isolated."""
    active = {side: len(_active(grouped.get((strip, side), []))) for side in SIDES}
    if any(count > 1 for count in active.values()):
        return "excluded"  # 同侧多份读数：先隔离，待复核员选定
    if any(count == 0 for count in active.values()):
        return "incomplete"
    return "pending"


def report(connection, code, strip, readings):
    """Merge instrument reports by plate + strip code; retries are idempotent."""
    created = connection.execute(
        "INSERT INTO strips(plate,code,state) VALUES(%s,%s,'incomplete') "
        "ON CONFLICT (plate,code) DO NOTHING RETURNING code",
        (code, strip),
    ).fetchone()
    # 串行化同一试条的两侧上报，合并结果才稳定。
    connection.execute(
        "SELECT 1 FROM strips WHERE plate=%s AND code=%s FOR UPDATE", (code, strip)
    ).fetchone()
    added = False
    for side, temp, density, fade in readings:
        inserted = connection.execute(
            "INSERT INTO strip_readings(plate,strip,side,temp,density,fade) "
            "VALUES(%s,%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING RETURNING id",
            (code, strip, side, temp, density, fade),
        ).fetchone()
        added = added or inserted is not None
    if added or created is not None:
        grouped = _grouped(connection, code, strip)
        connection.execute(
            "UPDATE strips SET state=%s WHERE plate=%s AND code=%s",
            (derive_state(grouped, strip), code, strip),
        )
    return one(connection, code, strip)


def _locked_strip(connection, code, strip):
    row = connection.execute(
        "SELECT * FROM strips WHERE plate=%s AND code=%s FOR UPDATE", (code, strip)
    ).fetchone()
    if row is None:
        raise HTTPException(404, "试条不存在")
    return row


def select(connection, code, strip, selection):
    """Keep one reading per side; every other reading stays on file as discarded.

    Once the pair is unambiguous again it returns to temperature-gap review.
    """
    strip = _locked_strip(connection, code, strip)
    rows = connection.execute(
        "SELECT * FROM strip_readings WHERE plate=%s AND strip=%s ORDER BY side,id FOR UPDATE",
        (code, strip["code"]),
    ).fetchall()
    by_id = {row["id"]: row for row in rows}
    chosen = {}
    for side, reading_id in selection.requested():
        row = by_id.get(reading_id)
        if row is None:
            raise HTTPException(409, "所选读数不属于该试条")
        if side is not None and row["side"] != side:
            raise HTTPException(409, "所选读数与这一侧不符")
        if row["state"] != "active":
            raise HTTPException(409, "该读数已裁掉，不能再选定")
        if row["side"] in chosen and chosen[row["side"]]["id"] != row["id"]:
            raise HTTPException(409, "每侧只能选定一条读数")
        chosen[row["side"]] = row
    for side in SIDES:
        if side in chosen:
            continue
        active = [row for row in rows if row["side"] == side and row["state"] == "active"]
        if len(active) > 1:
            raise HTTPException(409, f"{SIDE_NAMES[side]}同侧有多份读数，请先选定一条")
        chosen[side] = active[0] if active else None

    keep = {row["id"] for row in chosen.values() if row is not None}
    for row in rows:
        if row["state"] == "active" and row["id"] not in keep:
            connection.execute(
                "UPDATE strip_readings SET state='discarded' WHERE id=%s", (row["id"],)
            )
    state = "pending" if chosen["short"] and chosen["long"] else "incomplete"
    connection.execute(
        "UPDATE strips SET state=%s WHERE plate=%s AND code=%s",
        (state, code, strip["code"]),
    )
    return one(connection, code, strip["code"])


def classify(connection, code, strip, include):
    """Reviewer decision on a pair whose two sides are both unambiguous."""
    row = _locked_strip(connection, code, strip)
    grouped = _grouped(connection, code, row["code"])
    if any(len(_active(grouped.get((row["code"], side), []))) != 1 for side in SIDES):
        if any(len(_active(grouped.get((row["code"], side), []))) > 1 for side in SIDES):
            raise HTTPException(409, "同侧有多份读数，请先选定一条再复核")
        raise HTTPException(409, "两侧读数尚未补齐")
    short = _active(grouped[(row["code"], "short")])[0]
    long = _active(grouped[(row["code"], "long")])[0]
    record = {"short_temp": short["temp"], "long_temp": long["temp"]}
    connection.execute(
        "UPDATE strips SET state=%s WHERE plate=%s AND code=%s",
        (disposition(record, include), code, row["code"]),
    )
    return one(connection, code, row["code"])
