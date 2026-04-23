from databricks import sql
import os
from dotenv import load_dotenv

load_dotenv()

class DatabricksManager:
    def __init__(self):
        self._connection = None

    def connect(self):
        # first load to db will be slow as it needs to establish connection. subsequent calls will be faster.
        print("Connecting to Databricks...")
        return sql.connect(
            server_hostname=os.getenv("DATABRICKS_HOST"),
            http_path=os.getenv("DATABRICKS_HTTP_PATH"),
            client_id=os.getenv("DATABRICKS_CLIENT_ID"),
            client_secret=os.getenv("DATABRICKS_CLIENT_SECRET")
        )

    def get_conn(self):
        # check if connection exists. if not, connect
        if self._connection is None:
            self._connection = self.connect()
        
        # test if the connection is still alive
        try:
            # run a query to check health
            with self._connection.cursor() as cursor:
                cursor.execute("SELECT 1") 
        except Exception:
            print("Connection lost. Reconnecting...")
            self._connection = self.connect()
            
        return self._connection

# Create one instance to use everywhere
db_manager = DatabricksManager()