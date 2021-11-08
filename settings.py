import logging
import os

import dotenv  # type: ignore


dotenv.load_dotenv()

LOGGING_LEVEL = int(os.getenv("LOGGING_LEVEL", logging.INFO))
GITHUB_SECRET = os.getenv("GITHUB_SECRET", "")
GITHUB_UPDATES_CHAT_ID = os.getenv("GITHUB_UPDATES_CHAT_ID", 65960428)  # my own chat
