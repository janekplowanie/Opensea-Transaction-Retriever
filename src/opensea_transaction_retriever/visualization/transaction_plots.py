import matplotlib.pyplot as plt
from typing import List, Optional
import pandas as pd
from ..models.transaction import Transaction
from ..utils.time_utils import bin_transactions_by_time

def plot_price_history(transactions: List[Transaction], 
                      title: Optional[str] = None,
                      save_path: Optional[str] = None):
    """Plot price history over time."""
    df = pd.DataFrame([
        {'datetime': t.datetime, 'price': t.price_eth}
        for t in transactions
    ]).sort_values('datetime')
    
    plt.figure(figsize=(12, 6))
    plt.plot(df['datetime'], df['price'], marker='o', linestyle='-', alpha=0.6)
    plt.title(title or 'Price History')
    plt.xlabel('Date')
    plt.ylabel('Price (ETH)')
    plt.grid(True, alpha=0.3)
    
    if save_path:
        plt.savefig(save_path)
    plt.show()

def plot_volume_over_time(transactions: List[Transaction],
                         interval: str = 'D',
                         title: Optional[str] = None,
                         save_path: Optional[str] = None):
    """Plot transaction volume over time."""
    time_format = '%Y-%m-%d' if interval == 'D' else '%Y-%m'
    volume_data = bin_transactions_by_time(
        [t.__dict__ for t in transactions],
        time_format=time_format
    )
    
    dates = sorted(volume_data.keys())
    volumes = [volume_data[date] for date in dates]
    
    plt.figure(figsize=(12, 6))
    plt.bar(dates, volumes, alpha=0.7)
    plt.title(title or f'Transaction Volume by {interval}')
    plt.xlabel('Date')
    plt.ylabel('Number of Transactions')
    plt.xticks(rotation=45)
    plt.grid(True, alpha=0.3)
    
    if save_path:
        plt.savefig(save_path)
    plt.show()

def plot_price_distribution(transactions: List[Transaction],
                          bins: int = 50,
                          title: Optional[str] = None,
                          save_path: Optional[str] = None):
    """Plot distribution of transaction prices."""
    prices = [t.price_eth for t in transactions]
    
    plt.figure(figsize=(10, 6))
    plt.hist(prices, bins=bins, alpha=0.7)
    plt.title(title or 'Price Distribution')
    plt.xlabel('Price (ETH)')
    plt.ylabel('Frequency')
    plt.grid(True, alpha=0.3)
    
    if save_path:
        plt.savefig(save_path)
    plt.show()
