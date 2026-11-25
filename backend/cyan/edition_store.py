from fastapi import HTTPException

def plate(connection, code, lock=False):
    row=connection.execute("SELECT * FROM plates WHERE code=%s"+(" FOR UPDATE" if lock else ""),(code,)).fetchone()
    if not row:
        raise HTTPException(404,"试印版不存在")
    if lock and row["state"]!="open":
        raise HTTPException(409,"定版后试印批锁定")
    return row
