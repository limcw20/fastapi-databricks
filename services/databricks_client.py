import httpx
import time
from config import settings

_token_cache = {"token": None, "expires_at": 0}

async def get_access_token() -> str:
    if _token_cache["token"] and time.time() < _token_cache["expires_at"] - 30:
        return _token_cache["token"]

    url = f"{settings.databricks_host}/oidc/v1/token"
    async with httpx.AsyncClient() as client:
        r = await client.post(
            url,
            data={"grant_type": "client_credentials", "scope": "all-apis"},
            auth=(settings.databricks_client_id, settings.databricks_client_secret)
        )
        r.raise_for_status()
        data = r.json()
        _token_cache["token"] = data["access_token"]
        _token_cache["expires_at"] = time.time() + data.get("expires_in", 3600)
        return _token_cache["token"]

async def get_headers() -> dict:
    token = await get_access_token()
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }