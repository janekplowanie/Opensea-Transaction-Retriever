# Opensea-Transaction-Retriever
Opensea-Transaction-Retriever is a Python library that provides a selection of methods built around Opensea's API, enabling easier and more structured retrieval of NFT transactions and their metadata. This project contains functionalities required to retrieve and handle transaction data from Opensea, a digital marketplace for crypto collectibles and non-fungible tokens (NFTs) based on the ERC721 standard.

### Main Functionalities:

- Fetch transaction details for a specific collection within a time range and event type (e.g., successful sales).
- Extract and analyze NFT metadata, including traits.
- Calculate rarity scores for NFT traits based on their occurrence frequency.
- Save retrieved data in JSON format for further processing.

### Getting Started

To get a local copy of the project up and running on your local machine, please follow these steps.


1. Prerequisites: Ensure you have Python 3.10 installed. Download it from the official website if necessary https://www.python.org/downloads/.
2. Installation:
   -  Clone the repository and navigate to the project folder:
```shell
   git clone https://github.com/yourusername/your-repo.git
   
   cd Transaction_Retriever_Opensea
```
3. Setup:
   - Create a file named `.env` in the project directory.
   - Add an environment variable named `API_KEY` containing your OpenSea API key (refer to OpenSea's [documentation](https://docs.opensea.io/reference/api-keys) for obtaining an API key).
   - Example: `API_KEY = "your_api_key"`

### Wokrflow and Example Usage
1. Import the library:
```python
import pandas as pd
import json
from functions_and_methods import retrieve_transactions, get_traits_collection, get_nft_traits, add_rarity_score #...
```

2. Retrieve Transactions:

```python
# Replace with your desired collection slug, time range, event type, and filename
retrieve_transactions(collection_slug="cryptopunks", t_before="2010-12-10 12:34:00",t_after="2000-01-01 12:34:00", event_type="successful", file_name="CryptPunkTransactions")
```

3. Get collection Traits:

```python
# Replace with your collection slug
traits_file_path = get_traits_collection(collection_slug="cryptopunks")
# The traits data will be saved in the specified file path
```
4. Calculate rarity scores and example use:
```python
with open('Transaction_files/bored-ape-kennel-club.json') as a:
   trans_bakc = json.load(a)
   
df_bakc = pd.json_normalize(list_of_transactions_bakc)

# Downloading traits for a any single NFT 
df_bakc = get_nft_traits(df_bakc)

# Obtaining traits for bored-ape-kennel-club collection
get_traits_collection("bored-ape-kennel-club")

with open('Collection_traits/bored-ape-kennel-club_traits.json') as a:
   traits_bakc = json.load(a)
   
total_nfts_bakc = 10000 # Total supply of BAKC NFTs

# Based on the frequency of traits for BAKC, rarity score for trait is calculated
rarity_scores_bakc = calculate_rarity_scores(traits_bakc, total_nfts_bakc)

# Rarity score for any single NFT is calculated
add_rarity_score(df_bakc, rarity_scores_bakc)

# Processed transactions are stored as a json
df_bakc.to_json('Transactions_with_traits/df_bakc_traits.json', orient='records')
```
#### Now, you understand the main functionalities you can start using the project! 🔥 Hurray! 🔥

### Key Functions
#### To sum it up here are the key functions:
- `retrieve_transactions(collection_slug, t_before, t_after, event_type, file_name)`: Fetches transactions for a collection within a time range and event type, saving them to a JSON file.
- `get_traits_collection(collection_slug)`: Retrieves traits data for a collection from OpenSea and saves it to a JSON file.
- `extract_traits(url)`: Extracts NFT traits from a given URL containing NFT metadata.
- `get_nft_traits(transactions)`: Adds a column named 'nft.traits' to a pandas DataFrame containing extracted traits for each NFT.
- `calculate_rarity_scores(traits_data, total_nfts)`: Calculates rarity scores for each trait based on their occurrence frequency.
- `add_rarity_score(transactions, rarity_scores_collection)`: Adds a 'rarity_score' column to each transaction based on the provided rarity scores.

### Note:

Replace placeholders like `collection_slug`, `t_before`, `t_after`, and `file_name` with actual names and values.
Ensure you have a `.env` file containing the API Key.
### License

Distributed under the MIT License. See `LICENSE` for more information.
