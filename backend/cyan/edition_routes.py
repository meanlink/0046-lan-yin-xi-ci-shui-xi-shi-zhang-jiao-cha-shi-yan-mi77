from fastapi import APIRouter, Depends
from core import db, require
router=APIRouter(prefix="/cyan")

@router.get("/plates")
def plates(_actor=Depends(require())):
    with db() as connection:
        return connection.execute("SELECT * FROM plates ORDER BY code").fetchall()
