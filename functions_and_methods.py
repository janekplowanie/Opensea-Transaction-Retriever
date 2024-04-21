# %%
import requests
import json
import time
import calendar
import os
import pandas as pd
from dotenv import load_dotenv
from tenacity import retry, wait_exponential


def get_opsea_trans_by_collec(collection_slug: str, t_before: str, t_after: str, event_type: str,
                              file_name: str) -> None:
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
        # Extend the list by new transactions
        all_transactions.extend(transactions.get('asset_events', []))

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
        metadata = response.json()
        traits = metadata.get('counts', [])  # 2 keys in the dict: categories and counts

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

    max_retries = 3  # Maximum number of retries
    retries = 0

    while retries < max_retries:

        response = requests.get(url)

        if response.status_code == 200:

            metadata = response.json()
            traits = metadata.get('attributes', [])  # Returns a list of attributes
            return traits

        elif response.status_code == 429:  # Too Many Requests

            if 'Retry-After' in response.headers:
                retry_after = int(response.headers['Retry-After'])
                print(f"Rate limit exceeded. Waiting for {retry_after} seconds before retrying...")
                time.sleep(retry_after)  # Wait for the specified duration before retrying

            else:
                print("Rate limit exceeded. Waiting for a default duration before retrying...")
                time.sleep(10)  # Default wait time

            retries += 1
        else:
            print(f"Error extracting traits from {url}: Status Code {response.status_code}")
            return []

    print("Maximum number of retries reached. Aborting.")
    return []


# %%
def get_nft_traits(transactions: pd.DataFrame):
    """
   Retrieves traits for each unique NFT metadata URL and adds them to the transactions DataFrame.

   :param transactions: A pandas DataFrame containing NFT transaction data.
   :return: A pandas DataFrame with added 'nft.traits' column containing traits for each NFT.
   """

    # Check if 'nft.traits' column already exists
    if 'nft.traits' not in transactions.columns:
        transactions['nft.traits'] = None  # Initialize the column if it doesn't exist

    # Group DataFrame by unique NFT metadata URLs
    grouped = transactions.groupby('nft.metadata_url')  # print(grouped.ngroups) number of unique groups

    # Iterate over each group
    for url, group in grouped:
        # Extract traits for the current NFT
        # Each group corresponds to transactions associated with a unique NFT metadata URL
        traits = extract_traits(url)

        # Assign the extracted traits to the corresponding rows in the original DataFrame
        transactions.loc[group.index, 'nft.traits'] = len(group.index) * [[traits]]

    return transactions


#%%
def category_frequency(rarity_scores: dict) -> dict:
    """
    Sums the number of NFTs per trait category

    :param rarity_scores: A dictionary containing rarity scores for each trait category.
    :return: A dictionary containing the sum of NFTs per trait category
    """
    summed_scores = {}
    for category, traits in rarity_scores.items():
        summed_scores[category] = sum(traits.values())
    return summed_scores


#%%
def calculate_rarity_scores(traits_data: dict, total_nfts: int) -> dict:
    """
    Calculates the rarity scores for each trait based on the provided traits data.

    :param traits_data: A dictionary containing trait categories and their corresponding counts.
    :param total_nfts: Total number of NFTs.
    :return: A dictionary containing rarity scores for each trait.
    """
    rarity_scores = {}
    for category, traits in traits_data.items():  # Category ex. Background, Fur
        rarity_scores[category] = {}
        for trait, count in traits.items():
            rarity_scores[category][trait] = 1 / (count / total_nfts)
    return rarity_scores


#%%
def add_rarity_score(transactions: list, rarity_scores_collection: dict):
    """
    Add rarity scores to each transaction for a given collection based on rarity scores for a given trait.

    Args:
    - transactions (list): List of dictionaries representing transactions.
    - rarity_scores_collection (dict): Dictionary containing rarity scores for traits.

    Returns:
    - None: The function modifies transactions in place.
    """

    # Iterate over each dictionary in collection transaction
    for item in transactions:
        # Check if 'nft.traits' exists and is not None
        if item.get('nft.traits') is not None:
            # Extract trait values from 'nft.traits' and create a list of dictionaries
            traits = [{trait["trait_type"]: trait['value']} for trait in item['nft.traits']]

            # Initialize rarity score
            rarity_score = 0

            # Sum up rarity scores for each trait
            for trait_pair in traits:
                for key, value in trait_pair.items():
                    if key in rarity_scores_collection and value in rarity_scores_collection[key]:
                        rarity_score += rarity_scores_collection[key][value]

            # Add 'rarity_score' column to the current dictionary
            item['rarity_score'] = rarity_score


#%%
def get_opsea_trans_by_collec_experimental(collection_slug: str, t_before: str, t_after: str, event_type: str,
                                           file_name: str) -> None:
    """
    This is a newer implementation of `get_opsea_trans_by_collec` function.

    :param collection_slug: The slug of the collection on OpenSea.
    :param t_before: The timestamp of the latest transaction to fetch (inclusive), format 'Y-m-d H:M:S'.
    :param t_after: The timestamp of the earliest transaction to fetch (inclusive), format 'Y-m-d H:M:S'.
    :param event_type: The type of event to filter transactions (e.g., 'successful').
    :param file_name: The name of the file to save fetched transactions in JSON format.

    Note:
    -----
    - Make sure to create .env file in the Opensea-Transaction-Retriever directory where you create a string variable
      "API_KEY" with your actual Opensea API key, replace "my-collection" with the actual collection slug
      and adjust the time range and event type according to your requirements.
    """

    # Check for .env file
    if not os.path.isfile(".env"):
        raise FileNotFoundError(
            ".env file not found. Create a .env file with required environment variables.")

    # Load environment variables
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

    @retry(wait=wait_exponential(multiplier=2, min=1, max=8))  # Configure retry attempts with backoff
    def fetch_transactions(url):
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise for unsuccessful responses (e.g., 429)
        return response.json()

    while True:
        transactions = fetch_transactions(url)
        all_transactions.extend(transactions.get('asset_events', []))

        if 'next' in transactions and transactions['next']:
            next_transaction_number = transactions['next']
            url = f"{base_url}&next={next_transaction_number}"
        else:
            break

    # Save transactions to file
    with open(f'Transaction_files/{file_name}.json', 'w') as file:
        json.dump(all_transactions, file)

    end_time = time.time()
    elapsed_time_seconds = end_time - start_time
    elapsed_time_minutes = elapsed_time_seconds / 60
    print(f'The function took {elapsed_time_minutes} minutes to run')
    print(f"Fetched {len(all_transactions)} transactions")

#%%
