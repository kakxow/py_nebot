import logging
import os

import dotenv  # type: ignore


dotenv.load_dotenv()

LOGGING_LEVEL = int(os.getenv("LOGGING_LEVEL", logging.INFO))
