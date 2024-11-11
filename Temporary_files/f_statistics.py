import pandas
import pandas as pd
import json
from datetime import datetime
from collections import defaultdict
import matplotlib.pyplot as plt


def correlation_by_decile(df, column_deciles: str, column_correlations: str):
    """
    Calculates the correlation between rarity_score and percentage_return for each decile of rarity_score.

    Args:
        df (pandas.DataFrame): The DataFrame containing the data.

    Returns:
        pandas.Series: A Series containing the correlation coefficients for each decile.
    """
    # Discretize rarity_score into deciles
    deciles = pd.qcut(df[column_deciles], 10, labels=range(1, 11))

    # Group by deciles and calculate correlation
    correlation_by_decile = df.groupby(deciles)[column_deciles, column_correlations].corr(method='spearman')

    # Extract correlation for 'rarity_score' - 'percentage_return'
    return correlation_by_decile[column_deciles][column_correlations]


#%%
def plot_transaction_frequency_from_dataframe(df: pd.DataFrame, time_col: str, title: str):
    """
    Plots the frequency of transactions over time from a DataFrame.

    :param df: A pandas DataFrame containing transaction data.
    :param time_col: The column name containing timestamps in the DataFrame.
    :param title: The title for the transaction frequency plot.
    """
    # Assuming the timestamp is in UNIX format (seconds)
    df.loc[:, 'datetime'] = pd.to_datetime(df[time_col], unit='s', errors='coerce')
    # Create daily bins by setting hour, minute, and second to zero
    df.loc[:, 'date_bin'] = df['datetime'].dt.floor('D')
    # Group transactions by date bin and count occurrences
    transaction_counts = df.groupby('date_bin').size().to_frame(name='count')

    plt.figure(figsize=(12, 6))
    plt.plot(transaction_counts.index, transaction_counts['count'], linestyle='-')
    plt.xlabel('Date')
    plt.ylabel('Number of Transactions')
    plt.title(title)
    plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
    plt.tight_layout()
    plt.show()


#%%
def plot_transaction_frequency_and_avg_value(df: pd.DataFrame, time_col: str, value_col: str, title: str):
    """
    Plots the frequency and average value of transactions over time from a DataFrame.

    :param df: A pandas DataFrame containing transaction data.
    :param time_col: The column name containing timestamps in the DataFrame.
    :param value_col: The column name containing transaction values in the DataFrame.
    :param title: The title for the transaction frequency and average value plot.
    """
    # Assuming the timestamp is in UNIX format (seconds)
    # df['datetime'] = pd.to_datetime(df[time_col], unit='s')
    # # Create daily bins by setting hour, minute, and second to zero
    # df['date_bin'] = df['datetime'].dt.floor('D')

    # Assuming the timestamp is in UNIX format (seconds)
    df.loc[:, 'datetime'] = pd.to_datetime(df[time_col], unit='s', errors='coerce')
    # Create daily bins by setting hour, minute, and second to zero
    df.loc[:, 'date_bin'] = df['datetime'].dt.floor('D')

    # Group transactions by date bin
    grouped_transactions = df.groupby('date_bin')

    # Calculate daily transaction counts and average values
    transaction_counts = grouped_transactions.size()
    avg_values = grouped_transactions[value_col].median()  # before mean()

    fig, ax1 = plt.subplots(figsize=(12, 6))

    # Plot transaction counts on the primary axis
    ax1.plot(transaction_counts.index, transaction_counts, linestyle='-', color='r', label='Daily Transaction Count')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Number of Transactions', color='r')
    ax1.tick_params(axis='y', labelcolor='r')

    # Create a secondary axis for average value
    ax2 = ax1.twinx()
    ax2.plot(avg_values.index, avg_values, linestyle='-', color='g', label='Average Daily Value')
    ax2.set_ylabel('Average Value (Quantity)', color='g')
    ax2.tick_params(axis='y', labelcolor='g')

    # Add a legend for both axes
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')

    plt.title(title)
    plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
    plt.tight_layout()
    plt.show()


#%%
################################### JSON files LOADERS and METHODS ###################################
def load_json(full_file_path: str) -> list[dict]:
    """
    Loads transactions from a JSON file to a list of dictionaries.

    :param full_file_path: The name of the JSON file containing transactions.
    :return: A list of dictionaries representing transactions.
    """
    with open(f'{full_file_path}', 'r') as file:
        return json.load(file)


#%%
def load_json_pandas(full_file_path: str) -> pandas.DataFrame:
    """
    Loads transactions from a JSON file into a pandas DataFrame.

    :param full_file_path: The name of the JSON file containing transactions.
    :return: A pandas dataframe of transactions.
    """
    with open(f'{full_file_path}', 'r') as file:
        return pd.read_json(file)


#%%
def convert_unix_to_datetime(unix_timestamp: int) -> str:
    """
    Converts a UNIX timestamp to a human-readable date and time string.

    :param unix_timestamp: The UNIX timestamp in seconds.
    :return: A string representing the date and time in YYYY-MM-DD HH:MM:SS format.
    """
    return datetime.fromtimestamp(unix_timestamp).strftime('%Y-%m-%d %H:%MM:%S')


#%%
def bin_transactions_by_day(transactions: list[dict]) -> dict[str, int]:
    """
    Bins transactions by a specified time interval.

    :param transactions: A list of dictionaries representing transactions.
    :return: A dictionary where keys are time intervals in YYYY-MM-DD format and values are the number of transactions within that interval.
    """
    transaction_bins = defaultdict(int)
    for transaction in transactions:
        timestamp = transaction.get('event_timestamp')  # Assuming 'timestamp' key exists in the transaction dictionary
        if timestamp:
            # Convert timestamp to datetime and truncate to the beginning of the interval
            datetime_obj = datetime.fromtimestamp(timestamp)
            truncated_datetime = datetime_obj.replace(hour=0, minute=0, second=0, microsecond=0)
            time_bin = truncated_datetime.strftime('%Y-%m-%d')
            transaction_bins[time_bin] += 1
    return transaction_bins


#%%
def plot_transaction_frequency(transaction_bins: dict[str, int]) -> plt.Figure:
    """
    Plots the frequency of transactions over time.

    :param transaction_bins: A dictionary where keys are time intervals and values are the number of transactions within that interval.
    """
    time_bins = list(transaction_bins.keys())
    transaction_counts = list(transaction_bins.values())
    plt.figure(figsize=(10, 6))
    plt.plot(time_bins, transaction_counts, marker='o', linestyle='-')
    plt.xlabel('Time Interval')
    plt.ylabel('Number of Transactions')
    plt.title('Transaction Frequency by Day')
    plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
    plt.tight_layout()
    plt.show()

#%%
