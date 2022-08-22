from fastapi.exceptions import HTTPException


async def verify_offset(offset: int):
    if offset == 0:
        raise HTTPException(status_code=400, detail="Invalid offset value")


async def verify_limit(limit: int):
    if limit == 0:
        raise HTTPException(status_code=400, detail="Invalid limit value")
