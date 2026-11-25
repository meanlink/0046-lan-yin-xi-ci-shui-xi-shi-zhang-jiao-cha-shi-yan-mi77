from fastapi import APIRouter, Depends, HTTPException
from core import db, require
from cyan.edition_store import plate
from cyan.readings import Selection, StripSubmission
from cyan.strip_store import list_pairs, report, classify, select
router=APIRouter(prefix="/cyan/plates")


@router.get("/{code}/strips")
def list_strips(code:str,_actor=Depends(require())):
    with db() as connection:
        plate(connection,code)
        return list_pairs(connection,code)


@router.post("/{code}/strips",status_code=201)
def measure(code:str, submission:StripSubmission, _actor=Depends(require("operator"))):
    try:
        readings=submission.readings()
    except ValueError as exc:
        raise HTTPException(422,str(exc)) from exc
    with db() as connection:
        plate(connection,code,True)
        return report(connection,code,submission.code,readings)


@router.post("/{code}/strips/{strip}/select")
def select_reading(code:str,strip:str,selection:Selection,_actor=Depends(require("reviewer"))):
    with db() as connection:
        plate(connection,code,True)
        return select(connection,code,strip,selection)


@router.post("/{code}/strips/{strip}/qualify")
def qualify(code:str,strip:str,include:bool,_actor=Depends(require("reviewer"))):
    with db() as connection:
        plate(connection,code,True)
        return classify(connection,code,strip,include)
