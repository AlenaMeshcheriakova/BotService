from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):

    MODE: str
    BOT_TOKEN: str

    GRPC_HOST: str
    GRPC_PORT: int

    @property
    def get_GRPC_conn(self)-> str:
        return f"{self.GRPC_HOST}:{str(self.GRPC_PORT)}"


    model_config = SettingsConfigDict(env_file="../.env")

load_dotenv()
settings = Settings()