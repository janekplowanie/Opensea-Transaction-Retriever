from datetime import datetime
from typing import Union, Dict
from collections import defaultdict

def unix_to_datetime(unix_timestamp: int) -> datetime:
    """Convert Unix timestamp to datetime object."""
    return datetime.fromtimestamp(unix_timestamp)

def format_datetime(dt: Union[datetime, int], format: str = '%Y-%m-%d %H:%M:%S') -> str:
    """
    Format datetime object or Unix timestamp to string.
    
    Args:
        dt: datetime object or Unix timestamp
        format: datetime format string
    """
    if isinstance(dt, int):
        dt = unix_to_datetime(dt)
    return dt.strftime(format)

def bin_transactions_by_time(transactions: list, 
                           time_format: str = '%Y-%m-%d',
                           timestamp_key: str = 'event_timestamp') -> Dict[str, int]:
    """
    Group transactions by time interval.
    
    Args:
        transactions: List of transaction dictionaries
        time_format: Format string for the time bins
        timestamp_key: Key in transaction dict containing the timestamp
    
    Returns:
        Dictionary with time bins as keys and transaction counts as values
    """
    bins = defaultdict(int)
    for transaction in transactions:
        timestamp = transaction.get(timestamp_key)
        if timestamp:
            time_bin = format_datetime(timestamp, time_format)
            bins[time_bin] += 1
    return dict(bins)
