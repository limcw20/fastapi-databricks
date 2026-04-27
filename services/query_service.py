from db.connection import db_manager

def run_query(query: str, params=None) -> list[dict]:
    conn = db_manager.get_conn()
    with conn.cursor() as cursor:
        cursor.execute(query, params or [])
        columns = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()
        return [dict(zip(columns, row)) for row in rows]

def list_catalogs() -> list[dict]:
    return run_query("SHOW CATALOGS")

def list_schemas(catalog: str) -> list[dict]:
    return run_query(f"SHOW SCHEMAS IN {catalog}")

def list_tables(catalog: str, schema: str) -> list[dict]:
    return run_query(f"SHOW TABLES IN {catalog}.{schema}")