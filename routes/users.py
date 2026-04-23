from fastapi import APIRouter
from controllers.users import get_users

router = APIRouter()

@router.get("/")
def get_all_users():
    return get_users()
    