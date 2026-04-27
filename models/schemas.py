from pydantic import BaseModel
from typing import Optional

class UserRequest(BaseModel):
    email: str

class GrantRequest(BaseModel):
    principal: str
    catalog: str
    schema_name: Optional[str] = None
    table: Optional[str] = None
class RevokeRequest(BaseModel):
    principal: str
    catalog: str
    schema_name: Optional[str] = None
    table: Optional[str] = None