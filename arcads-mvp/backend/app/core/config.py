from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "postgresql+psycopg://postgres:postgres@localhost:5432/arcads"
    redis_url: str = "redis://localhost:6379/0"
    aws_region: str = "us-east-1"
    s3_bucket: str = "arcads"
    s3_endpoint_url: str | None = None
    aws_access_key_id: str | None = None
    aws_secret_access_key: str | None = None
    cors_origins: str = "http://localhost:3000"
    openai_api_key: str | None = None
    elevenlabs_api_key: str | None = None
    avatar_api_key: str | None = None

settings = Settings()