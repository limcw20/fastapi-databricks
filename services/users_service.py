import httpx
from services.databricks_client import get_headers
from config import settings

async def get_user(email: str) -> dict | None:
    url = f"{settings.databricks_host}/api/2.0/preview/scim/v2/Users"
    async with httpx.AsyncClient() as client:
        r = await client.get(
            url,
            headers=await get_headers(),
            params={"filter": f'userName eq "{email}"'}
        )
        r.raise_for_status()
        users = r.json().get("Resources", [])
        return users[0] if users else None

async def add_user(email: str) -> dict:
    url = f"{settings.databricks_host}/api/2.0/preview/scim/v2/Users"
    payload = {
        "schemas": ["urn:ietf:params:scim:schemas:core:2.0:User"],
        "userName": email,
        "emails": [{"value": email, "primary": True}],
        "active": True
    }
    async with httpx.AsyncClient() as client:
        r = await client.post(url, headers=await get_headers(), json=payload)
        r.raise_for_status()
        return r.json()