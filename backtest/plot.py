import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
from numpy import float64
import pandas as pd

from tools import load_data, grid_bb


def plot_candlestick(ax, data, width=0.001):
    '''
    Строит свечной график (candlestick) на переданной оси (ax).

    Parameters:
        ax (matplotlib.axes.Axes): Ось, на которой будет построен график.
        data (pd.DataFrame): Датафрейм с данными для построения графика (должен содержать столбцы 'Date', 'Open', 'High', 'Low', 'Close').
        width (float, optional): Ширина баров (свечей). По умолчанию 0.001.

    Returns:
        None: Функция строит график непосредственно на переданной оси.
    '''
    for i in range(len(data)):
        # Извлекаем данные для каждой свечи
        date, open_price, high, low, close = data.iloc[i][:5]

        # Определяем цвет свечи (зеленая для восходящей, красная для нисходящей)
        color = 'green' if data.iloc[i, 4] > data.iloc[i, 1] else 'red'

        # Рисуем вертикальную линию (high и low)
        ax.vlines(date, low, high, color=color, linewidth=1)

        # Рисуем бар (свечу) с цветом и размерами, основанными на цене открытия и закрытия
        ax.bar(date, abs(close - open_price), width, bottom=min(open_price, close), color=color, edgecolor=color)


def plot_grids(ax, grid):
    date = grid['Date']
    for col in grid_df.columns.to_list()[:-1]:
        ax.plot(date, grid_df[col], color='black')


if __name__ == '__main__':
    # Загружаем данные
    data = load_data('data/ETHUSDT_60.csv', start_dt='2025-05-20', end_dt='2025-05-30')

    # Загружаем сетку
    grid = grid_bb(data['Close'], grid_cnt=4, length=20, mult=2)
    grid_data = {f'grid_{i}': grid[i] for i in range(len(grid))}
    grid_data['Date'] = data['Date']
    grid_df = pd.DataFrame(grid_data)

    fig, ax = plt.subplots(figsize=(24, 12))

    # Настройка формата отображения временных меток на оси X
    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d %H:%M'))
    ax.xaxis_date()  # Ось X будет интерпретироваться как временные метки

    # Рисуем Supertrend и свечи
    plot_candlestick(ax, data, 0.03)
    plot_grids(ax, grid_df)

    plt.xticks(rotation=30)  # Поворот меток времени
    plt.tight_layout()  # Автоматически подгоняет график для улучшения отображения

    plt.savefig("plot.png")
    print('=== ГРАФИК СОЗДАН ===')