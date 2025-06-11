from containers import Container

if __name__ == "__main__":
    container = Container()
    bybit_api = container.bybit_api()

    print(bybit_api.user.get_balance())
