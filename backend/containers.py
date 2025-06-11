from dependency_injector import containers, providers

from services import get_logger, BybitAPI


class Container(containers.DeclarativeContainer):
    logger = providers.Singleton(get_logger)
    bybit_api = providers.Factory(BybitAPI, logger=logger)
