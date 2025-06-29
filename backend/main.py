from containers import Container

if __name__ == "__main__":
    container = Container()
    bybit_api = container.bybit_api()

    # last_price = bybit_api.market.get_last_price('BTCUSDT', '30')
    print(bybit_api.trade.place_order('BTCUSDT', 'Buy', 0.00005))
