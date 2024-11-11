# API Reference

## OpenSeaClient

The main interface for interacting with OpenSea's API.

### Initialization
```python
from opensea_transaction_retriever import OpenSeaClient

client = OpenSeaClient(api_key="your_api_key")  # Direct API key
# OR
client = OpenSeaClient()  # Uses API_KEY from environment variables
```

### Methods

#### get_collection_transactions
```python
def get_collection_transactions(
    collection_slug: str, 
    t_before: str, 
    t_after: str, 
    event_type: str = "successful",
    save_to_file: Optional[str] = None
) -> List[Transaction]
```
Fetches transactions for a collection within a specified time range.

Parameters:
- `collection_slug`: Collection identifier (e.g., "boredapeyachtclub")
- `t_before`: End time in format 'YYYY-MM-DD HH:MM:SS'
- `t_after`: Start time in format 'YYYY-MM-DD HH:MM:SS'
- `event_type`: Type of event (default: "successful")
- `save_to_file`: Optional path to save raw JSON data

#### get_collection
```python
def get_collection(collection_slug: str) -> Collection
```
Retrieves collection metadata.

#### calculate_collection_rarity
```python
def calculate_collection_rarity(collection_slug: str) -> Dict[str, List[Dict]]
```
Calculates rarity scores for all traits in a collection.

## Models

### Transaction
```python
@dataclass
class Transaction:
    transaction_hash: str
    event_timestamp: int
    total_price: float
    payment_token: Dict[str, Any]
    seller_address: str
    buyer_address: str
    collection_slug: str
    nft_id: str
    nft_metadata_url: Optional[str] = None
    nft_traits: Optional[List[Dict[str, Any]]] = None
    rarity_score: Optional[float] = None
```

### Trait
```python
@dataclass
class Trait:
    trait_type: str
    value: str
    count: int
    rarity_score: float = 0.0
```

### Collection
```python
@dataclass
class Collection:
    slug: str
    name: str
    total_supply: int
    traits: Optional[Dict[str, List[Trait]]] = None
```

## Visualization Functions

### Transaction Plots

#### plot_price_history
```python
def plot_price_history(
    transactions: List[Transaction], 
    title: Optional[str] = None,
    save_path: Optional[str] = None
)
```

#### plot_volume_over_time
```python
def plot_volume_over_time(
    transactions: List[Transaction],
    interval: str = 'D',
    title: Optional[str] = None,
    save_path: Optional[str] = None
)
```

### Trait Analysis

#### plot_trait_distribution
```python
def plot_trait_distribution(
    traits: Dict[str, List[Trait]],
    trait_type: str,
    title: Optional[str] = None,
    save_path: Optional[str] = None
)
```

#### plot_rarity_scores
```python
def plot_rarity_scores(
    traits: Dict[str, List[Trait]],
    trait_type: str,
    title: Optional[str] = None,
    save_path: Optional[str] = None
)
```