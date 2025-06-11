import logging

from pybit.unified_trading import HTTP


class UserAPI:
    def __init__(self, client: HTTP, logger: logging.Logger):
        self.client = client
        self.logger = logger

    def get_balance(self, coin: str = "USDT", symbol: str = "BTCUSDT", margin: bool = False) -> float:
        '''Получает баланс указанной валюты на счете.'''

        self.logger.debug(f"⌛️ Запрос на получение баланса...")

        result = 0.0
        try:
            # Выполняем запрос к API для получения баланса
            if margin:
                response = self.client.get_borrow_quota(category="spot", symbol=symbol, side="Sell")
                result = float(response['result']['maxTradeAmount'])
            else:
                response = self.client.get_wallet_balance(accountType="UNIFIED", coin=coin)
                result = float(response['result']['list'][0]['coin'][0]['walletBalance'])
        except Exception as e:
            # Логируем ошибку, если запрос не удался
            self.logger.error(f"❌ Ошибка при API запросе: {e}")
            return 0
        
        self.logger.debug(f"✅ Баланс получен: {result}")
        return result
