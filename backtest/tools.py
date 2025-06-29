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


def linreg(y: pd.Series, length: int) -> pd.Series:
    """
    Возвращает линию линейной регрессии (аналог ta.linreg в Pine Script).
    
    Parameters:
        y (pd.Series): Ценовой ряд (например, Close).
        length (int): Длина окна.
    
    Returns:
        pd.Series: Кривая линейной регрессии (ŷ) той же длины.
    """
    def _linreg(values):
        x = np.arange(len(values))
        y = np.array(values)
        if len(y) != length or np.isnan(y).any():
            return np.nan
        slope, intercept = np.polyfit(x, y, 1)
        return intercept + slope * x[-1]  # ŷ в последней точке окна

    return y.rolling(length).apply(_linreg, raw=False)


def bollinger_bands(src: pd.Series, length: int, mult: float, length_bbw: int) -> pd.DataFrame:
    # Основная линия: линейная регрессия
    basis = linreg(src, length)
    
    # Стандартное отклонение
    dev = mult * src.rolling(length).std()

    upper = basis + dev
    lower = basis - dev

    bbw = (upper - lower) / basis * 100

    # Сглаженный bbw
    check_bbw = linreg(bbw, length_bbw)

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


def get_data(length: int, mult: float, length_bbw: int, start_dt=None, end_dt=None):
    # Загружаем данные
    d_15 = load_data('data/ETHUSDT_15.csv', start_dt, end_dt)
    d_60 = load_data('data/ETHUSDT_60.csv', start_dt, end_dt)

    # Расчитываем полосы Боллинджера
    bb = bollinger_bands(d_60['Close'], length, mult, length_bbw)
    d_60 = d_60.join(bb)

    return d_15, d_60


if __name__ == '__main__':
    d_15, d_60 = get_data(20, 2, 100)
    print(d_60)
