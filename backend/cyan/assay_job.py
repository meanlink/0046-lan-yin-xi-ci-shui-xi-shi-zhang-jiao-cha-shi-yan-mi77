from cyan.cohort import sample
from cyan.criteria import eligible
from cyan.edition_store import plate
from cyan.sign_flip import estimate

def run(connection,kind,payload):
    if kind!="cyanotype-test":
        raise ValueError(kind)
    code=payload["code"]
    trial=plate(connection,code,True)
    rows,fingerprint=sample(connection,code)
    gain,p=estimate([r["long_density"]-r["short_density"] for r in rows])
    fade=max(float(r["long_fade"]) for r in rows)
    return connection.execute(
        "INSERT INTO assays(plate,sample_key,gain,p,fade,n,eligible) VALUES(%s,%s,%s,%s,%s,%s,%s) RETURNING *",
        (code,fingerprint,gain,p,fade,len(rows),eligible(gain,p,fade,trial["fade_limit"]))).fetchone()
