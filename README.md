# OpenSea Transaction Retriever

A Python library for retrieving and analyzing NFT transactions from OpenSea.

## Features

- Fetch NFT transactions with detailed metadata
- Calculate trait rarity scores
- Generate visualization plots
- Export data in various formats

## Installation

### For Users

```bash
# Create a new virtual environment
python -m venv opensea-venv

# Activate the virtual environment
# On Windows:
opensea-venv\Scripts\activate
# On macOS/Linux:
source opensea-venv/bin/activate 

# Install the package (will also install all required dependencies)
pip install opensea-transaction-retriever
```

## Quick Start

```python
from opensea_transaction_retriever import OpenSeaClient

# Initialize client
client = OpenSeaClient(api_key="your_opensea_api_key")

# Fetch transactions
transactions = client.get_collection_transactions(
    collection_slug="boredapeyachtclub",
    t_before="2024-01-01 00:00:00",
    t_after="2023-12-01 00:00:00"
)
```

## Documentation
For detailed documentation, see the [docs](docs/) directory:
- [API Reference](docs/api.md)
- [Usage Guide](docs/usage.md)


### For Developers

```bash
# Clone the repository
git clone https://github.com/janekplowanie/Opensea-Transaction-Retriever.git
cd Opensea-Transaction-Retriever

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .

# Run tests
pytest tests/
```

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.