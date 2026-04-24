from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    databricks_host: str
    databricks_http_path: str
    databricks_client_id: str
    databricks_client_secret: str

    class Config:
        env_file = ".env"

settings = Settings()