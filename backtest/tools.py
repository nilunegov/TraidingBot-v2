import numpy as np
import pandas as pd


def load_data(filepath: str, start_dt=None, end_dt=None) -> pd.DataFrame:
    '''
    Загружаем данные для анализа, выбирая определенные столбцы,
    преобразуя временные метки и сбрасывая индекс.

    :param data: Исходный DataFrame, содержащий финансовые данные.
    :return: pd.DataFrame: Обработанный DataFrame с выбранными столбцами, преобразованными
    временными метками и сброшенным индексом.
    '''

    data = pd.read_csv(filepath)

    # Определяем список необходимых столбцов
    columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']

    # Создаем копию исходного DataFrame с выбранными столбцами
    data = data[columns].copy()

    # Преобразуем столбец 'Date' в тип datetime
    data['Date'] = pd.to_datetime(data['Date'])

    # Выбираем нужный временной интервал
    if start_dt and end_dt:
        data = data[(start_dt <= data['Date']) & (data['Date'] <= end_dt)]
    elif start_dt and not(end_dt):
        data = data[data['Date'] >= start_dt]
    elif not(start_dt) and end_dt:
        data = data[data['Date'] <= end_dt]

    # Сбрасываем индекс и возвращаем обработанный DataFrame
    return data.reset_index(drop=True)


def sync_dfs(frames: list):
    pass


def lz(series: pd.Series, lzf: float) -> pd.Series:
    lz_values = []
    prev_lz = None

    for i in range(len(series)):
        x = series.iloc[i]

        if pd.isna(x):
            lz_values.append(np.nan)
            continue

        if prev_lz is None:
            prev_lz = x
            lz_values.append(x)
            continue

        s = np.sign(x)
        upper = prev_lz + lzf * abs(prev_lz) * s
        lower = prev_lz - lzf * abs(prev_lz) * s

        if i > 0 and x == series.iloc[i - 1]:
            lz_val = x
        elif x > upper or x < lower:
            lz_val = x
        else:
            lz_val = prev_lz

        prev_lz = lz_val
        lz_values.append(lz_val)

    return pd.Series(lz_values, index=series.index)



def wma(series: pd.Series, length: int) -> pd.Series:
    weights = np.arange(1, length + 1)
    wma = series.rolling(window=length).apply(lambda x: np.dot(x, weights) / weights.sum(), raw=True)
    return wma


def lazy_bollinger_bands(src: pd.Series, length: int, mult: float, length_bbw: int, lzf: float) -> pd.DataFrame:
    basis = wma(src, length)

    # Стандартное отклонение
    dev = mult * src.rolling(length).std()

    upper = lz(basis + dev, lzf)
    lower = lz(basis - dev, lzf)

    bbw = (upper - lower) / basis * 100

    # Сглаженный bbw
    check_bbw = bbw.rolling(length_bbw).mean()

    return pd.DataFrame({
        "basis": basis,
        "upper": upper,
        "lower": lower,
        "bbw": bbw,
        "check_bbw": check_bbw
    })


def bollinger_bands(src: pd.Series, length: int, mult: float, length_bbw: int) -> pd.DataFrame:
    # Основная линия: линейная регрессия
    basis = wma(src, length)
    
    # Стандартное отклонение
    dev = mult * src.rolling(length).std()

    upper = basis + dev
    lower = basis - dev

    bbw = (upper - lower) / basis * 100

    # Сглаженный bbw
    check_bbw = bbw.rolling(length_bbw).mean()

    return pd.DataFrame({
        "basis": basis,
        "upper": upper,
        "lower": lower,
        "bbw": bbw,
        "check_bbw": check_bbw
    })

def grid_bb(src: pd.Series, grid_cnt: int, length: int, mult: float) -> list:
    grid_lst = [None for _ in range(grid_cnt + 1)]
    mult_step = mult / grid_cnt * 2

    basis = linreg(src, length)
    dev = src.rolling(length).std()
    
    for i in range(grid_cnt // 2):
        d = mult * dev
        u = basis + d
        l = basis - d
        grid_lst[i] = l
        grid_lst[grid_cnt - i] = u
        mult -= mult_step
    grid_lst[grid_cnt // 2] = basis

    return grid_lst


def get_data(length: int, mult: float, length_bbw: int, lzf: float, start_dt=None, end_dt=None):
    # Загружаем данные
    d_60 = load_data('data/ETHUSDT_D.csv', start_dt, end_dt)

    # Расчитываем полосы Боллинджера
    bb = lazy_bollinger_bands(d_60['Close'], length, mult, length_bbw, lzf)
    d_60 = d_60.join(bb)

    return d_60


if __name__ == '__main__':
    d_15, d_60 = get_data(5, 2, 5, 0.05)
    print(d_60)
