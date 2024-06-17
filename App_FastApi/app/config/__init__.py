from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://{}:{}@{}:{}/{}"
    test: bool = False
    project_name: str = "SkyPulse"
    



settings = Settings()  # type: ignore
