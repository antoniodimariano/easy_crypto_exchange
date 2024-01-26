from os import getenv
from dotenv import load_dotenv
import app.core.logging_config
from app.core.config import Settings, Setup

load_dotenv(getenv("ENV_FILE"))

settings = Settings()
setup = Setup()
