from containers import Container

if __name__ == "__main__":
    container = Container()
    bybit_api = container.bybit_api()

    print(bybit_api.data.get_data("BTCUSDT", '30', 100))
