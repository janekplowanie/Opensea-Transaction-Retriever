import pytest
from datetime import datetime, timedelta
from opensea_transaction_retriever import OpenSeaClient

@pytest.fixture
def client():
    return OpenSeaClient()

def test_client_initialization():
    """Test client initialization with missing API key."""
    with pytest.raises(ValueError):
        OpenSeaClient(api_key=None)

def test_get_collection(client):
    """Test fetching collection metadata."""
    collection = client.get_collection("boredapeyachtclub")
    assert collection.slug == "boredapeyachtclub"
    assert collection.total_supply > 0

def test_get_transactions(client):
    """Test fetching transactions."""
    end_time = datetime.now()
    start_time = end_time - timedelta(hours=1)
    
    transactions = client.get_collection_transactions(
        collection_slug="boredapeyachtclub",
        t_before=end_time.strftime('%Y-%m-%d %H:%M:%S'),
        t_after=start_time.strftime('%Y-%m-%d %H:%M:%S')
    )
    
    assert isinstance(transactions, list)
