import os
from pathlib import Path

from dotenv import load_dotenv


load_dotenv(Path(__file__).resolve().parents[1] / ".env")


DEFAULT_BASE_URL = os.getenv("BONBONITE_BASE_URL", "https://www.bon-bonite.com")
TEST_LOGIN_DOCUMENT = os.getenv("BONBONITE_TEST_DOCUMENT", "")
TEST_LOGIN_PASSWORD = os.getenv("BONBONITE_TEST_PASSWORD", "")