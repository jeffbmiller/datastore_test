from pydantic import BaseSettings


class Settings(BaseSettings):
    service_account_path: str

    class Config:
        env_file = ".env"