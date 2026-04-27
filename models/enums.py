from enum import Enum

class SecurableType(str, Enum):
    CATALOG = "catalog"
    SCHEMA = "schema"
    TABLE = "table"
    VIEW = "view"

class Privilege(str, Enum):
    USE_CATALOG = "USE_CATALOG"
    USE_SCHEMA = "USE_SCHEMA"
    SELECT = "SELECT"
    MODIFY = "MODIFY"
    CREATE_SCHEMA = "CREATE_SCHEMA"
    CREATE_TABLE = "CREATE_TABLE"
    ALL_PRIVILEGES = "ALL_PRIVILEGES"