import logging
import os

from pybit.unified_trading import HTTP


class TradeAPI:
    def __init__(self, client: HTTP, logger: logging.Logger):
        self.client = client
        self.logger = logger

    def place_order(self, symbol: str, side: str, size: float) -> dict:
        """
        Размещает ордер.

        Parameters:
            symbol (str): Символ криптовалютной пары для ордера (например, 'BTCUSDT').
            side (str): Направление ордера ('Buy' или 'Sell').
            size (float): Размер ордера.

        Returns:
            dict: Ответ за запрос
        """

        self.logger.debug(f"⌛️ Запрос на размещение ордера...")

        order_param = {
            "category": "spot",
            "symbol": symbol,
            "side": side,
            "orderType": "Market",
            "qty": size,
            "marketUnit": "baseCoin",
            "timeInForce": "GTC",
            "isLeverage": 1,
        }

        try:
            response = self.client.place_order(**order_param)
        except Exception as e:
            self.logger.error(f"❌ Ошибка при API запросе: {e}")
            return False

        if response["retMsg"] == "OK":
            self.logger.debug(f"✅ Ордер успешно установлен!")
        else:
            self.logger.warning(f"⚠  Что-то пошло не так...")

        return response

    def place_tp(self, sympol: str, side: str, size: float, price: float, order_link_id: str):
        """
        Размещает ордер на тейк-профит (TP) на указанном символе.

        Parameters:
            symbol (str): Символ криптовалютной пары для ордера (например, 'BTCUSDT').
            side (str): Направление ордера ('Buy' или 'Sell').
            size (float): Размер ордера.
            price (float): Цена срабатывания ордера (триггерная цена для тейк-профита).

        Returns:
            str: Ответ от API о статусе ордера или None в случае ошибки.
        """

        order_param = {
            "category": "spot",
            "symbol": sympol,
            "side": side,
            "orderType": "Market",
            "qty": size,
            "marketUnit": "baseCoin",
            "orderFilter": "tpslOrder",  # Указание на ордер типа тейк-профит
            "triggerPrice": price,
            "orderLinkId": order_link_id,
            "timeInForce": "GTC",
        }

        try:
            response = self.client.place_order(**order_param)
        except Exception as e:
            self.logger.error(f"❌ Ошибка при API запросе: {e}")
            return None

        self.logger.debug(f"✅ Тейк-профит установлен")

        return response
