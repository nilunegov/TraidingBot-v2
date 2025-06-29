import logging
import os

from pybit.unified_trading import HTTP

from .account import AccountAPI
from .market import MarketAPI
from .trade import TradeAPI

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
LEVERAGE = os.getenv("LEVERAGE")


class BybitAPI:
    def __init__(self, logger: logging.Logger):
        client = HTTP(
            testnet=False,
            api_key=API_KEY,
            api_secret=API_SECRET
        )
        
        client.spot_margin_trade_toggle_margin_trade(spotMarginMode="1")
        client.spot_margin_trade_set_leverage(leverage=LEVERAGE)

        self.account = AccountAPI(client, logger)
        self.market = MarketAPI(client, logger)
        self.trade = TradeAPI(client, logger)