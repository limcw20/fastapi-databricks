from databricks import sql
from config import settings

class DatabricksManager:
    def __init__(self):
        self._connection = None

    def connect(self):
        print("Connecting to Databricks...")
        return sql.connect(
            server_hostname=settings.databricks_host,
            http_path=settings.databricks_http_path,
            client_id=settings.databricks_client_id,
            client_secret=settings.databricks_client_secret
        )

    def get_conn(self):
        if self._connection is None:
            self._connection = self.connect()
        try:
            with self._connection.cursor() as cursor:
                cursor.execute("SELECT 1")
        except Exception:
            print("Connection lost. Reconnecting...")
            self._connection = self.connect()
        return self._connection

    def close(self):
        if self._connection:
            self._connection.close()
            self._connection = None

db_manager = DatabricksManager()