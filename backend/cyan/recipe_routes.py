from fastapi import APIRouter, Depends
from core import db, require
from cyan.signature import sign
router=APIRouter(prefix="/cyan")

@router.get("/recipes")
def recipes(_actor=Depends(require())):
    with db() as connection:
        return connection.execute("SELECT * FROM recipes ORDER BY plate").fetchall()

@router.post("/plates/{code}/recipe",status_code=201)
def finalize(code:str,assay:int,actor=Depends(require("reviewer"))):
    with db() as connection:
        return sign(connection,code,assay,actor["email"])
