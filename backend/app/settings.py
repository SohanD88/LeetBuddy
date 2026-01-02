from pydantic import BaseModel
import os

class Settings(BaseModel):
    openai_api_key: str
    supabase_jwt_secret: str


def get_settings() -> Settings:
    return Settings(
        openai_api_key=os.environ["OPENAI_API_KEY"],
        supabase_jwt_secret=os.environ["SUPABASE_JWT_SECRET"],
    )