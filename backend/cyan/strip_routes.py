from fastapi import APIRouter, Depends
from core import db, require
from cyan.edition_store import plate
from cyan.readings import Strip
from cyan.strip_store import list_pairs, insert, classify
router=APIRouter(prefix="/cyan/plates")

@router.get("/{code}/strips")
def list_strips(code:str,_actor=Depends(require())):
    with db() as connection:
        plate(connection,code)
        return list_pairs(connection,code)

@router.post("/{code}/strips",status_code=201)
def measure(code:str, strip:Strip, _actor=Depends(require("operator"))):
    with db() as connection:
        plate(connection,code,True)
        return insert(connection,code,strip)

@router.post("/{code}/strips/{strip}/qualify")
def qualify(code:str,strip:str,include:bool,_actor=Depends(require("reviewer"))):
    with db() as connection:
        plate(connection,code,True)
        return classify(connection,code,strip,include)
