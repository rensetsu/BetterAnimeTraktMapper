import os

from dotenv import load_dotenv

load_dotenv()

SIMKL_CLIENT_ID = os.getenv("SIMKL_CLIENT_ID")
TRAKT_CLIENT_ID = os.getenv("TRAKT_CLIENT_ID")
USER_AGENT = "github-batm/0.0.1 (https://github.com/nattadasu/BetterAnimeTraktMapper)"
