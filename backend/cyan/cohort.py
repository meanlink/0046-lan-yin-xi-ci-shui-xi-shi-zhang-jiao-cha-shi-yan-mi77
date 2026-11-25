from hashlib import sha256
from fastapi import HTTPException
from cyan.strip_store import list_pairs

def sample(connection,code):
    rows=list_pairs(connection,code)
    if any(row["state"] in ("pending","incomplete") for row in rows):
        raise HTTPException(409,"仍有未复核试条或未补齐的读数")
    selected=[r for r in rows if r["state"]=="paired"]
    if not 6<=len(selected)<=16:
        raise HTTPException(409,"需要 6 至 16 个有效配对")
    fingerprint=[(r["code"],r["short"]["id"],r["long"]["id"]) for r in selected]
    return selected,sha256(repr(fingerprint).encode()).hexdigest()
