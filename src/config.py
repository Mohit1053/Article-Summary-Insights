import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application configuration loaded from environment variables."""

    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY", "")
        self.model = os.getenv("MODEL", "gpt-4o-mini")
        self.output_dir = os.getenv("OUTPUT_DIR", "outputs")


settings = Settings()