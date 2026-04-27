import httpx
from typing import Literal
from services.databricks_client import get_headers
from models.enums import SecurableType, Privilege
from config import settings

async def update_grant(
    securable_type: SecurableType,
    full_name: str,
    principal: str,
    privileges: list[Privilege],
    action: Literal["add", "remove"] = "add"
):
    # securable_type must be lowercase: "catalog", "schema", "table"
    url = f"{settings.databricks_host}/api/2.1/unity-catalog/permissions/{securable_type.value}/{full_name}"
    payload = {"changes": [{"principal": principal, action: [p.value for p in privileges]}]}
    async with httpx.AsyncClient() as client:
        r = await client.patch(url, headers=await get_headers(), json=payload)
        r.raise_for_status()
        return r.json()

async def grant_read_access(principal: str, catalog: str, schema_name: str = None, table: str = None):
    await update_grant(SecurableType.CATALOG, catalog, principal, [Privilege.USE_CATALOG])
    if schema_name:
        await update_grant(SecurableType.SCHEMA, f"{catalog}.{schema_name}", principal, [Privilege.USE_SCHEMA])
    if table and schema_name:
        await update_grant(SecurableType.TABLE, f"{catalog}.{schema_name}.{table}", principal, [Privilege.SELECT])

async def revoke_access(principal: str, catalog: str, schema_name: str = None, table: str = None):
    if table and schema_name:
        await update_grant(SecurableType.TABLE, f"{catalog}.{schema_name}.{table}", principal, [Privilege.SELECT], action="remove")
    if schema_name:
        await update_grant(SecurableType.SCHEMA, f"{catalog}.{schema_name}", principal, [Privilege.USE_SCHEMA], action="remove")
    await update_grant(SecurableType.CATALOG, catalog, principal, [Privilege.USE_CATALOG], action="remove")