# test_data_api.py

from unittest.mock import Mock

import pandas as pd
import pytest
from services import DataAPI


@pytest.fixture
def mock_logger():
    return Mock()


@pytest.fixture
def mock_client():
    return Mock()


def test_get_data_success(mock_client, mock_logger):
    candles_data = [
        [1620000000000, "100", "110", "90", "105", "1000", "105000"],
        [1620000060000, "105", "115", "95", "110", "1200", "132000"],
    ]
    mock_client.get_kline.return_value = {"result": {"list": candles_data}}

    api = DataAPI(mock_client, mock_logger)
    df = api.get_data("BTCUSDT", "1", 2)

    assert isinstance(df, pd.DataFrame)
    assert len(df) == 2
    assert list(df.columns) == [
        "Date",
        "Open",
        "High",
        "Low",
        "Close",
        "Volume",
        "Turnover",
    ]
    assert df["Close"].iloc[0] == 110.0
    mock_logger.debug.assert_called()
    mock_logger.info.assert_called()


def test_get_data_api_exception(mock_client, mock_logger):
    mock_client.get_kline.side_effect = Exception("API Error")

    api = DataAPI(mock_client, mock_logger)
    df = api.get_data("BTCUSDT", "1", 2)

    assert isinstance(df, pd.DataFrame)
    assert df.empty
    mock_logger.error.assert_called_once()
    mock_logger.warning.assert_called_once()


def test__get_candles_success(mock_client, mock_logger):
    expected_data = [
        [1620000000000, "100", "110", "90", "105", "1000", "105000"],
        [1620000060000, "105", "115", "95", "110", "1200", "132000"],
    ]
    mock_client.get_kline.return_value = {"result": {"list": expected_data}}

    api = DataAPI(mock_client, mock_logger)
    result = api._get_candles("BTCUSDT", "1", 2)

    assert result == expected_data
    mock_client.get_kline.assert_called_once_with(
        category="spot", symbol="BTCUSDT", interval="1", limit=2
    )
    mock_logger.debug.assert_called()


def test__get_candles_exception(mock_client, mock_logger):
    mock_client.get_kline.side_effect = Exception("Connection timeout")

    api = DataAPI(mock_client, mock_logger)
    result = api._get_candles("BTCUSDT", "1", 2)

    assert isinstance(result, pd.DataFrame)
    assert result.empty
    assert list(result.columns) == [
        "Date",
        "Open",
        "High",
        "Low",
        "Close",
        "Volume",
        "Turnover",
    ]
    mock_logger.error.assert_called_once()
