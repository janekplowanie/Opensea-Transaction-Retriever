# Usage Guide

## Getting Started

### Installation

1. Create a virtual environment:
```bash
python -m venv opensea-venv
source opensea-venv/bin/activate  # On Windows: opensea-venv\Scripts\activate
```

2. Install the package:
```bash
pip install opensea-transaction-retriever
```

### Setting Up API Access

1. Get an API key from OpenSea
2. Set it as an environment variable:
```bash
export API_KEY=your_api_key
```
Or use it directly in code:
```python
client = OpenSeaClient(api_key="your_api_key")
```

## Basic Operations

### Fetching Transactions

```python
from opensea_transaction_retriever import OpenSeaClient
from datetime import datetime, timedelta

# Initialize client
client = OpenSeaClient()

# Set time range
end_time = datetime.now()
start_time = end_time - timedelta(days=7)

# Format times
t_before = end_time.strftime('%Y-%m-%d %H:%M:%S')
t_after = start_time.strftime('%Y-%m-%d %H:%M:%S')

# Fetch transactions
transactions = client.get_collection_transactions(
    collection_slug="boredapeyachtclub",
    t_before=t_before,
    t_after=t_after
)
```

### Analyzing Traits and Rarity

```python
# Get collection traits
collection = client.get_collection("boredapeyachtclub")

# Calculate rarity scores
trait_rarity = client.calculate_collection_rarity("boredapeyachtclub")

# Visualize trait distribution
from opensea_transaction_retriever.visualization import plot_trait_distribution
plot_trait_distribution(trait_rarity, "Background")
```

## Data Visualization

### Price Analysis
```python
from opensea_transaction_retriever.visualization import (
    plot_price_history,
    plot_volume_over_time,
    plot_price_distribution
)

# Plot price history
plot_price_history(transactions, title="BAYC Price History")

# Plot trading volume
plot_volume_over_time(transactions, interval='D')

# Plot price distribution
plot_price_distribution(transactions, bins=50)
```

### Trait Analysis
```python
from opensea_transaction_retriever.visualization import (
    plot_trait_distribution,
    plot_rarity_scores,
    plot_trait_correlation
)

# Plot trait distributions
plot_trait_distribution(trait_rarity, "Background")

# Plot rarity scores
plot_rarity_scores(trait_rarity, "Background")

# Plot trait-price correlation
plot_trait_correlation(transactions, "Background")
```

## Best Practices

1. **Rate Limiting**: The client handles rate limiting automatically, but be mindful of API limits

2. **Data Storage**: Save raw data for later analysis:
```python
transactions = client.get_collection_transactions(
    collection_slug="boredapeyachtclub",
    t_before=t_before,
    t_after=t_after,
    save_to_file="transactions.json"
)
```

3. **Error Handling**: The client includes retry logic for failed requests

4. **Resource Management**: Use context managers:
```python
with OpenSeaClient() as client:
    transactions = client.get_collection_transactions(...)
```

## Common Issues and Solutions

1. **API Key Issues**
```python
# Check if API key is set
import os
print("API key is set:", bool(os.getenv("API_KEY")))
```

2. **Rate Limiting**
The client automatically handles rate limiting with exponential backoff

3. **Data Processing**
Use pandas for advanced analysis:
```python
import pandas as pd
df = pd.DataFrame([t.__dict__ for t in transactions])
```
