from fastapi import APIRouter, Depends
from core import db,enqueue,require
from cyan.edition_store import plate
from cyan.cohort import sample
router=APIRouter(prefix="/cyan/plates")

@router.get("/{code}/assays")
def read(code:str,_actor=Depends(require())):
    with db() as connection:
        return connection.execute("SELECT * FROM assays WHERE plate=%s ORDER BY id DESC",(code,)).fetchall()

@router.post("/{code}/assays",status_code=202)
def calculate(code:str,_actor=Depends(require("reviewer"))):
    with db() as connection:
        plate(connection,code,True)
        sample(connection,code)
        return {"job_id":enqueue(connection,"cyanotype-test",{"code":code})}
