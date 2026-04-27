from fastapi import APIRouter, HTTPException
from models.schemas import UserRequest
from services import users_service
import httpx

router = APIRouter()

@router.post("/")
async def add_user(req: UserRequest):
    try:
        existing = await users_service.get_user(req.email)
        if existing:
            return {"status": "already_exists", "user": existing}
        user = await users_service.add_user(req.email)
        return {"status": "created", "user": user}
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)

@router.get("/{email}")
async def get_user(email: str):
    try:
        user = await users_service.get_user(email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
