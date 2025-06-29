# test_user_api.py

import pytest
from unittest.mock import Mock
from services import AccountAPI


@pytest.fixture
def mock_logger():
    return Mock()


@pytest.fixture
def mock_client():
    return Mock()


def test_get_balance_spot_success(mock_client, mock_logger):
    # Мокаем ответ API
    mock_client.get_wallet_balance.return_value = {
        'result': {'list': [{'coin': [{'walletBalance': '123.45'}]}]}
    }

    api = AccountAPI(mock_client, mock_logger)
    balance = api.get_balance(coin="USDT", margin=False)

    assert balance == 123.45
    mock_logger.debug.assert_called()
    mock_client.get_wallet_balance.assert_called_once()


def test_get_balance_margin_success(mock_client, mock_logger):
    mock_client.get_borrow_quota.return_value = {
        'result': {'maxTradeAmount': '200.5'}
    }

    api = AccountAPI(mock_client, mock_logger)
    balance = api.get_balance(symbol="BTCUSDT", margin=True)

    assert balance == 200.5
    mock_client.get_borrow_quota.assert_called_once()
    mock_logger.debug.assert_called()


def test_get_balance_api_exception(mock_client, mock_logger):
    mock_client.get_wallet_balance.side_effect = Exception("API failed")

    api = AccountAPI(mock_client, mock_logger)
    balance = api.get_balance()

    assert balance == 0
    mock_logger.error.assert_called_once()
