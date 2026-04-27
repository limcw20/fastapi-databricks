from fastapi import FastAPI
from routes import users, permissions, provision
from db.connection import db_manager
import httpx
from services.databricks_client import get_headers
from config import settings

app = FastAPI()

app.include_router(users.router, prefix="/users")
app.include_router(permissions.router, prefix="/grants")
app.include_router(provision.router, prefix="/provision")


@app.get("/whoami")
async def whoami():
    async with httpx.AsyncClient() as client:
        r = await client.get(
            f"{settings.databricks_host}/api/2.0/preview/scim/v2/Me",
            headers=await get_headers()
        )
        return r.json()

@app.on_event("shutdown")
async def shutdown():
    db_manager.close()