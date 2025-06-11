import logging

from pybit.unified_trading import HTTP


class OrderAPI:
    def __init__(self, client: HTTP, logger: logging.Logger):
        self.client = client
        self.logger = logger

    def place_order(self, symbol: str, side: str, size: float) -> str:
        pass
