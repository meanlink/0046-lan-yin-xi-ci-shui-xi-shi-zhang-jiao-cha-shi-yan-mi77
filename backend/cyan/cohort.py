from hashlib import sha256
from fastapi import HTTPException
from cyan.strip_store import list_pairs

def sample(connection,code):
    rows=list_pairs(connection,code)
    if any(row["state"]=="pending" for row in rows):
        raise HTTPException(409,"仍有未复核试条")
    selected=[r for r in rows if r["state"]=="paired"]
    if not 6<=len(selected)<=16:
        raise HTTPException(409,"需要 6 至 16 个有效配对")
    return selected,sha256(repr(selected).encode()).hexdigest()
