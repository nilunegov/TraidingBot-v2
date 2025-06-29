import os
import time
import warnings
from datetime import datetime, timedelta

import pandas as pd
from pybit.unified_trading import HTTP

warnings.filterwarnings("ignore")

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

# Create HTTP-client
client = HTTP(testnet=False, api_key=API_KEY, api_secret=API_SECRET)


def _get_candles(symbol: str, interval: str, limit: int, start_time: int) -> list:
    """
    Получение исторических данных свечей с Bybit через pybit.

    :param symbol: Торговая пара, например, "BTCUSDT".
    :param interval: Таймфрейм свечей ("1", "5", "15", "30", "60", и т.д.).
    :param limit: Количество свечей (максимум 1000 на запрос).
    :param start_time: Время начала (timestamp в миллисекундах).
    :return list: Список со свечами
    """

    print(f"🔎 Запрос на получение данных для {symbol} ({interval}) с сайта ByBit...")

    try:
        response = client.get_kline(
            category="spot",  # Используем спотовую торговлю
            symbol=symbol,
            interval=interval,
            limit=limit,
            start=start_time,
        )

        print(
            f"✅ Успешно получены {len(response["result"]["list"])} свечей для {symbol} ({interval}) с сайта ByBit!"
        )
        return response["result"]["list"]

    except Exception as e:
        print(f"❌ Ошибка при получении данных с API: {e}")

    return pd.DataFrame(
        columns=["Date", "Open", "High", "Low", "Close", "Volume", "Turnover"]
    )


def _process_candle(data: list) -> pd.DataFrame:
    """
    Вспомогательная функция. Преобразует список в датафрейм

    :param data: Значения свеч в формате (Date, Open, High, Low, Close, Volume, Turnover)
    :param columns: Название колонок, если формат другой
    :return: DataFrame
    """
    print(f"🔄 Обработка данных...")

    columns = ["Date", "Open", "High", "Low", "Close", "Volume", "Turnover"]

    df = pd.DataFrame(data[::-1], columns=columns)

    # Преобразуем дату в понятную для датафрейма тип
    df["Date"] = pd.to_datetime(pd.to_numeric(df["Date"]), unit="ms")

    for col in columns[1:]:  # Преобразуем все, кроме 'Date'
        df[col] = df[col].astype(float)

    print(f"✅ Данные успешно обработаны!")
    return df


def get_kline(symbol: str, interval: str, limit: int, start_time: int) -> pd.DataFrame:
    """
    Получение исторических данных с Bybit.

    :param symbol: Торговая пара, например, "BTCUSDT".
    :param interval: Таймфрейм свечей ("1", "5", "15", "30", "60", и т.д.).
    :param limit: Количество свечей (максимум 1000 на запрос).
    :param start_time: Время начала (timestamp в миллисекундах).
    :return DataFrame: DataFrame с историческими свечами (Date, Open, High, Low, Close, Volume, Turnover)
    """

    candles = _get_candles(symbol, interval, limit, start_time)
    candles = _process_candle(candles)

    if candles.empty:
        print(f"⚠ Данные пустые!")

    return candles


def append_to_csv(df, filepath):
    file_exists = os.path.isfile(filepath)
    write_header = not file_exists or os.stat(filepath).st_size == 0

    df.to_csv(filepath, mode="a", header=write_header, index=False)


def get_historical_kline(
    symbol: str, interval: str, start_time: str, end_time: str
) -> pd.DataFrame:
    start_time = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
    end_time = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")

    # Разница в миллисекундах
    delta = int((end_time - start_time).total_seconds() * 1000)
    # Количество запросов
    i = int(interval) * 60 * 1000
    cnt_request = delta // i
    if delta % i != 0:
        cnt_request += 1

    print("=== СБОР ДАННЫХ ===\n")

    filepath = f"data/{symbol}_{interval}.csv"
    if os.path.exists(filepath):
        os.remove(filepath)

    while cnt_request > 0:
        time.sleep(2)

        limit = 1000 if cnt_request >= 1000 else cnt_request + 1
        end_dt = start_time + timedelta(milliseconds=i * limit)

        print(
            f"⌛️ Получение данных для {symbol} ({interval}) за период [{start_time} - {end_dt}]"
        )
        tmp = get_kline(symbol, interval, limit, int(start_time.timestamp() * 1000))
        append_to_csv(tmp, filepath)

        start_time = end_dt
        cnt_request -= limit
        print()
    print("=== СБОР ЗАВЕРШЕН ===\n")


if __name__ == "__main__":
    get_historical_kline("ETHUSDT", "60", "2025-03-01 00:00:00", "2025-06-01 00:00:00")
