from fastapi import HTTPException
from cyan.pairing import disposition

def list_pairs(connection,code):
    return connection.execute("SELECT * FROM strips WHERE plate=%s ORDER BY code",(code,)).fetchall()

def insert(connection, code, strip):
    return connection.execute(
        "INSERT INTO strips(plate,code,short_temp,long_temp,short_density,long_density,long_fade) "
        "VALUES(%s,%s,%s,%s,%s,%s,%s) RETURNING *",(code,*strip.model_dump().values())).fetchone()

def classify(connection,code,strip,include):
    row=connection.execute("SELECT * FROM strips WHERE plate=%s AND code=%s",(code,strip)).fetchone()
    if row is None:
        raise HTTPException(404,"试条不存在")
    return connection.execute("UPDATE strips SET state=%s WHERE plate=%s AND code=%s RETURNING *",
        (disposition(row,include),code,strip)).fetchone()
