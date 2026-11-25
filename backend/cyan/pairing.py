from fastapi import HTTPException

def disposition(record, include):
    if include and abs(record["short_temp"]-record["long_temp"])>2:
        raise HTTPException(409,"两片水温差超过 2°C，须隔离")
    return "paired" if include else "excluded"
