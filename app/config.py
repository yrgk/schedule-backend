import os

from dotenv import load_dotenv

load_dotenv()

class Settings:
    DSN = os.getenv("DSN")
    START_DAY = "02.09.2026"
    IS_ODD_START_DAY_WEEK = True
    DATE_FORMAT = "%d.%m.%Y"