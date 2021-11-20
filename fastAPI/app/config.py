from pydantic import BaseSettings


class Settings(BaseSettings):
    """This is used to validate all the environment variables."""

    DATABASE_HOST: str
    DATABASE_USER: str
    DATABASE_NAME: str
    DATABASE_PORT: str
    DATABASE_PASSWORD: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRATION_MINUTES: int

    class Config:
        """Used to import the .env file"""
        env_file = ".env"


# instantiate the Settings class
settings = Settings()
