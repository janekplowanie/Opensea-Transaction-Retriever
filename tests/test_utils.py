import pytest
from datetime import datetime
from opensea_transaction_retriever.utils import (
    unix_to_datetime,
    format_datetime,
    bin_transactions_by_time
)

def test_unix_to_datetime():
    """Test Unix timestamp conversion."""
    timestamp = 1640995200  # 2022-01-01 00:00:00
    dt = unix_to_datetime(timestamp)
    assert isinstance(dt, datetime)
    assert dt.year == 2022
    assert dt.month == 1
    assert dt.day == 1

def test_bin_transactions():
    """Test transaction binning by time."""
    transactions = [
        {"event_timestamp": 1640995200},  # 2022-01-01
        {"event_timestamp": 1640995200},  # 2022-01-01
        {"event_timestamp": 1641081600},  # 2022-01-02
    ]
    
    bins = bin_transactions_by_time(transactions)
    assert len(bins) == 2
    assert bins["2022-01-01"] == 2
    assert bins["2022-01-02"] == 1
