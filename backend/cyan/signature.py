from fastapi import HTTPException
from cyan.edition_store import plate
from cyan.cohort import sample

def sign(connection,code,assay,actor):
    trial=plate(connection,code,True)
    _,fingerprint=sample(connection,code)
    result=connection.execute("SELECT * FROM assays WHERE plate=%s AND id=%s",(code,assay)).fetchone()
    if not result or result["sample_key"]!=fingerprint:
        raise HTTPException(409,"试条有变，须重算后签发")
    if not result["eligible"]:
        raise HTTPException(409,"密度或掉色未达到定版限值")
    receipt=connection.execute(
        "INSERT INTO recipes(plate,assay,wash_sec,signer) VALUES(%s,%s,%s,%s) RETURNING *",
        (code,assay,trial["long_sec"],actor)).fetchone()
    connection.execute("UPDATE plates SET state='sealed' WHERE code=%s",(code,))
    return receipt
