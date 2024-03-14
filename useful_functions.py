# %%
import requests
import json
import time
import calendar
import os
import pandas as pd
from dotenv import load_dotenv


def get_opsea_trans_by_collec(collection_slug: str, t_before: str, t_after: str, event_type: str, file_name: str):
    """
    :param collection_slug: A string representing the slug of the collection on OpenSea.
    :param t_before: A string representing the timestamp of the latest transaction to fetch (inclusive),
    time format: 'Y-m-d H:M:S'.
    :param t_after: A string representing the timestamp of the earliest transaction to fetch (inclusive),
    time format: 'Y-m-d H:M:S'.
    :param event_type: A string representing the type of event to filter the transactions (e.g., 'successful').
    :param file_name: A string representing the name of the file in which to save the fetched transactions in JSON format.
    :return: None

    This method fetches all the transactions for a given collection on OpenSea within a specific time range and event type.
    It retrieves the transactions using pagination and saves the fetched transactions to a JSON file.

    Example Usage:
    --------------
    >>> get_opsea_trans_by_collec("cryptopunks", "2010-12-10 12:34:00", "2000-01-01 12:34:00", "sale", "Transactions_June_October")

    Note:
    -----
    - Make sure to create .env file in the Opensea-Transaction-Retriever directory where you create a string variable
      "API_KEY" with your actual Opensea API key, replace "my-collection" with the actual collection slug
      and adjust the time range and event type according to your requirements.
    """

    # Check if .env file exists
    if not os.path.isfile(".env"):
        raise FileNotFoundError(
            ".env file not found. Please create a .env file with the required environment variables.")

    # Load environment variables from .env file
    load_dotenv()
    api_key = os.getenv("API_KEY")

    start_time = time.time()

    t_after_unix = calendar.timegm(time.strptime(t_after, '%Y-%m-%d %H:%M:%S'))
    t_before_unix = calendar.timegm(time.strptime(t_before, '%Y-%m-%d %H:%M:%S'))

    url = f"https://api.opensea.io/api/v2/events/collection/{collection_slug}?after={t_after_unix}&before={t_before_unix}&event_type={event_type}"
    base_url = url
    headers = {
        "accept": "application/json",
        "x-api-key": api_key
    }

    all_transactions = []

    while True:
        response = requests.get(url, headers=headers)
        transactions = response.json()
        # Append transactions to the list
        all_transactions.append(transactions)

        if 'next' in transactions and transactions['next']:  # deleted: is not None
            next_transaction_number = transactions['next']
            url = f"{base_url}&next={next_transaction_number}"
        else:
            break  # Break the loop if there's no 'next' field or it's None

    # Save all transactions to the Transaction_files folder
    with open(f'Transaction_files/{file_name}.json', 'w') as file:
        json.dump(all_transactions, file)

    end_time = time.time()
    elapsed_time_seconds = end_time - start_time
    elapsed_time_minutes = elapsed_time_seconds / 60
    print(f'The function took {elapsed_time_minutes} minutes to run')


# %%

def list_of(list_of_data, trans_block, element):
    """
    :param list_of_data: A variable that contains a list of transaction blocks.
    :param trans_block: The key indicating the transaction block number.
    :param element: The key indicating the element to be printed from the asset_events list.

    :return: list of values for the given element
    """
    list_of_values = []
    for i in range(0, len(list_of_data[trans_block]['asset_events'])):
        list_of_values.append(list_of_data[trans_block]['asset_events'][i][element])

    return list_of_values


# %%
def myenumerator(x, column):
    """
    :param x: list, the input list or dataframe
    :param column: int or str, the column index or name to be enumerated
    :return: None

    Enumerates the elements in the specified column of the input list or dataframe.
    The function iterates over the elements in the specified column of the input list or dataframe using the enumerate() function.
    Each element is assigned a unique index starting from 0. The function then prints the index and the corresponding element.

    Example Usage:
    --------------
    >>> x = {'A': [10, 20, 30], 'B': [40, 50, 60]}
    >>> column = 'A'
    >>> myenumerator(x, column)
    Entry n: 0 , 10
    Entry n: 1 , 20
    Entry n: 2 , 30

    Note:
    -----
    - The input column can be specified either as an index or a column name.
    - The function does not return any value, it only prints the enumerated entries.

    """
    for index, transaction in enumerate(x[column]):
        print(f'Entry n: {index} , {transaction} \n')


# %%
def extract_and_print_keys_from_dict(d: dict):
    """
    Extracts and prints all keys from a nested dictionary.

    :param d: The dictionary to extract keys from.
    :type d: dict
    :return: None
    """

    def extract_keys(d, parent_key=''):
        keys = []
        for k, v in d.items():
            new_key = f"{parent_key}.{k}" if parent_key else k
            keys.append(new_key)
            if isinstance(v, dict):
                keys.extend(extract_keys(v, new_key))
        return keys

    keys = extract_keys(d)

    # Printing the keys
    for key in keys:
        print(key)


# %%
def extract_asset_events(dict_list: list):
    """
    Extracts asset events from a list of dictionaries.

    :param dict_list: A list of dictionaries.
    :return: A list of asset events (transactions) extracted from the input dictionaries.
    """
    asset_events_list = []
    for item in dict_list:
        if 'asset_events' in item:
            asset_events_list.extend(item['asset_events'])
    return asset_events_list


# %%
def how_long(file_data):
    """
    Calculate the total number of asset events in the given file_data.

    :param file_data: The data containing the asset events.
    :return: The total number of asset events in the file_data.

    """
    event_count = sum(len(block['asset_events']) for block in file_data)
    return event_count


# %%
def combine_json_files(file_names: list, output_file: str):
    combined_data = []

    for file_name in file_names:
        with open(f'Transaction_files/{file_name}.json', 'r') as file:
            transactions = json.load(file)
            combined_data.extend(transactions)

    # Save combined data to a new file
    with open(f'Transaction_files/{output_file}.json', 'w') as output_file:
        json.dump(combined_data, output_file)


# %%
def get_traits_collection(collection_slug: str):
    """
    Retrieves traits for a given collection from the OpenSea API and saves them to a JSON file.

    :param collection_slug: A string representing the slug of the collection on OpenSea.
    :return: A string representing the file path where the traits JSON file is saved.
    """

    # Check if .env file exists
    if not os.path.isfile(".env"):
        raise FileNotFoundError(
            ".env file not found. Please create a .env file with the required environment variables.")

    # Load environment variables from .env file
    load_dotenv()
    api_key = os.getenv("API_KEY")

    url = f"https://api.opensea.io/api/v2/traits/{collection_slug}"

    headers = {
        "accept": "application/json",
        "x-api-key": api_key
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        # Create a directory to store the JSON file if it doesn't exist
        directory = "Collection_traits"
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Save response to a JSON file
        file_path = os.path.join(directory, f"{collection_slug}_traits.json")
        traits = response.json()
        with open(file_path, 'w') as file:
            json.dump(traits, file)

        return file_path
    else:
        print(f"Failed to retrieve traits for collection {collection_slug}. Status code: {response.status_code}")
        return None


# %%
def extract_traits(url):
    """
    Extracts NFT traits from a given URL containing NFT metadata.

    :param url: A string representing the URL containing NFT metadata.
    :return: A list of dictionaries representing the traits extracted from the metadata.
    """

    response = requests.get(url)
    if response.status_code == 200:
        metadata = response.json()
        traits = metadata.get('attributes', [])
        return traits
    else:
        print(f"Error extracting traits from {url}: Status Code {response.status_code}")
        return []


# %%
def get_nft_traits(transactions: pd.DataFrame):
    """
   Retrieves traits for each unique NFT metadata URL and adds them to the transactions DataFrame.

   :param transactions: A pandas DataFrame containing NFT transaction data.
   :return: A pandas DataFrame with added 'nft.traits' column containing traits for each NFT.
   """

    # Group DataFrame by unique NFT metadata URLs
    grouped = transactions.groupby('nft.metadata_url')  # print(grouped.ngroups) number of unique groups

    # Dictionary to store NFT metadata URLs and corresponding traits
    nft_traits = {}

    # Iterate over each group
    for url, group in grouped:
        # Extract traits for the current NFT
        # Each group corresponds to transactions associated with a unique NFT metadata URL
        traits = extract_traits(url)
        # Store traits for the current NFT
        nft_traits[url] = traits

    # Create a new DataFrame with NFT metadata URLs and their traits
    df_nft_traits = pd.DataFrame({'nft.metadata_url': list(nft_traits.keys()), 'nft.traits': list(nft_traits.values())})

    # Merge the new DataFrame with the original transactions DataFrame
    df_merged = pd.merge(transactions, df_nft_traits, on='nft.metadata_url', how='left')

    return df_merged

#%%
