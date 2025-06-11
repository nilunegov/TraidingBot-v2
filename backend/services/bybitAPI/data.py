import logging
import pandas as pd

from pybit.unified_trading import HTTP


class DataAPI:
    def __init__(self, client: HTTP, logger: logging.Logger):
        self.client = client
        self.logger = logger

    def _get_candles(self, symbol: str, interval: str, limit: int) -> list:
        """
        Получение исторических данных свечей с Bybit через pybit.

        :param symbol: Торговая пара, например, "BTCUSDT".
        :param interval: Таймфрейм свечей ("1", "5", "15", "30", "60", и т.д.).
        :param limit: Количество свечей (максимум 1000 на запрос).
        :param start_time: Время начала (timestamp в миллисекундах).
        :return list: Список со свечами
        """

        self.logger.debug(
            f"⌛️ Запрос на получение данных для {symbol} ({interval}) с сайта ByBit..."
        )

        try:
            response = self.client.get_kline(
                category="linear",  # Используем фьючерсную торговлю
                symbol=symbol,
                interval=interval,
                limit=limit,
            )

            self.logger.debug(
                f"✅ Успешно получены {len(response["result"]["list"])} свечей для {symbol} ({interval}) с сайта ByBit!"
            )
            return response["result"]["list"]

        except Exception as e:
            self.logger.error(f"❌ Ошибка при получении данных с API: {e}")

        return pd.DataFrame(
            columns=["Date", "Open", "High", "Low", "Close", "Volume", "Turnover"]
        )

    def _process_candle(self, data: list) -> pd.DataFrame:
        """
        Вспомогательная функция. Преобразует список в датафрейм

        :param data: Значения свеч в формате (Date, Open, High, Low, Close, Volume, Turnover)
        :param columns: Название колонок, если формат другой
        :return: DataFrame
        """
        self.logger.debug(f"⌛️ Обработка данных...")

        columns = ["Date", "Open", "High", "Low", "Close", "Volume", "Turnover"]

        df = pd.DataFrame(data[::-1], columns=columns)

        # Преобразуем дату в понятную для датафрейма тип
        df["Date"] = pd.to_datetime(df["Date"], unit="ms")

        for col in columns[1:]:  # Преобразуем все, кроме 'Date'
            df[col] = df[col].astype(float)
        
        self.logger.debug(f"✅ Данные успешно обработаны!")
        return df
    
    def get_data(self, symbol: str, interval: str, limit: int) -> pd.DataFrame:
        '''
        Получение исторических данных с Bybit.

        :param symbol: Торговая пара, например, "BTCUSDT".
        :param interval: Таймфрейм свечей ("1", "5", "15", "30", "60", и т.д.).
        :param limit: Количество свечей (максимум 1000 на запрос).
        :param start_time: Время начала (timestamp в миллисекундах).
        :return DataFrame: DataFrame с историческими свечами (Start, Open, High, Low, Close, Volume, Turnover)
        '''
        self.logger.info(f"⌛️ Получение данных для {symbol} ({interval}) с сайта ByBit...")

        candles = self._get_candles(symbol, interval, limit)
        candles = self._process_candle(candles)

        if candles.empty:
            self.logger.warning(f"⚠ Данные пустые!")
        else:
            self.logger.info(f"✅ Данные успешно получены!")
        return candles
