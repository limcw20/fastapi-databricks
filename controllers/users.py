from db.connection import db_manager

def get_users():
    conn = db_manager.get_conn()
    
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM dev_catalog.app_data.users")
        
        # fetch as an Arrow Table
        arrow_table = cursor.fetchall_arrow()
        
        # convert to a list of dictionaries
        # .to_pylist() is the PyArrow way to get a JSON-serializable list
        result = arrow_table.to_pylist()
        
        return {"users": result}