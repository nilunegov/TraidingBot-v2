import logging
import os

from pybit.unified_trading import HTTP

from .user import UserAPI
from .data import DataAPI

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")


class BybitAPI:
    def __init__(self, logger: logging.Logger):
        client = HTTP(
            testnet=False,
            api_key=API_KEY,
            api_secret=API_SECRET
        )
        self.user = UserAPI(client, logger)
        self.data = DataAPI(client, logger)