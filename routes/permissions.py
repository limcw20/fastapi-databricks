from fastapi import APIRouter, HTTPException
from models.schemas import GrantRequest, RevokeRequest
from services import grants_service
import httpx

router = APIRouter()

@router.post("/")
async def grant_access(req: GrantRequest):
    try:
        await grants_service.grant_read_access(
            req.principal, req.catalog, req.schema_name, req.table
        )
        return {"status": "granted", "principal": req.principal}
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)

@router.delete("/")
async def revoke_access(req: RevokeRequest):
    try:
        await grants_service.revoke_access(
            req.principal, req.catalog, req.schema_name, req.table
        )
        return {"status": "revoked", "principal": req.principal}
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)