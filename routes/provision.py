from fastapi import APIRouter, HTTPException
from models.schemas import ProvisionRequest
from services import users_service, grants_service
import httpx

router = APIRouter()

@router.post("/")
async def provision_user(req: ProvisionRequest):
    try:
        # Cannot add user since not in premium workspace
        # existing = await users_service.get_user(req.principal)
        # if not existing:
        #     await users_service.add_user(req.principal)
        await grants_service.grant_read_access(
            req.principal, req.catalog, req.schema_name, req.table
        )
        return {"status": "provisioned", "user": req.principal}
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
    