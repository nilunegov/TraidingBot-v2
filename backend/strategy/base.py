from abc import ABC, abstractmethod
from typing import Any, Dict


class Strategy(ABC):
    def __init__(self, symbol: str, parameters: Dict[str, Any]):
        """
        :param symbol: Торговый инструмент (например, 'BTC/USDT')
        :param parameters: Параметры стратегии (например, длина скользящей средней и т.д.)
        """
        self.symbol = symbol
        self.parameters = parameters
        
    @abstractmethod
    def on_tick(self) -> None:
        """
        Вызывается на каждый новый тик или свечу.
        """
        pass

    @abstractmethod
    def fetch_market_data(self) -> bool:
        '''Получение актуальных данных, обновление бд и csv'''
        pass

    @abstractmethod
    def get_signal(self) -> str:
        '''
        Возвращает сигнал действия
        * short
        * exit
        * long
        * hold
        * change_tp
        '''
        pass
    
    @abstractmethod
    def should_short(self) -> bool:
        '''Возвращает True, если стратегия считает, что нужно ставить шорт.'''
        pass

    @abstractmethod
    def should_long(self) -> bool:
        '''Возвращает True, если стратегия считает, что нужно ставить лонг.'''
        pass

    @abstractmethod
    def should_change_tp(self) -> bool:
        '''Возвращает True, если стратегия считает, что нужно сменить tp.'''
        pass

    @abstractmethod
    def should_exit(self) -> bool:
        '''Возвращает True, если стратегия считает, что нужно выходить.'''
        pass

    @abstractmethod
    def place_order(self) -> bool:
        '''Размещает ордер'''
        pass