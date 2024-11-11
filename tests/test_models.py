import pytest
from opensea_transaction_retriever.models import Transaction, Trait, Collection

def test_transaction_from_api():
    """Test Transaction model creation from API response."""
    api_data = {
        "transaction_hash": "0x123",
        "event_timestamp": 1640995200,
        "total_price": "1000000000000000000",
        "payment_token": {"decimals": 18},
        "seller": {"address": "0x456"},
        "buyer": {"address": "0x789"},
        "collection": {"slug": "test-collection"},
        "nft": {"identifier": "1"}
    }
    
    transaction = Transaction.from_api_response(api_data)
    assert transaction.transaction_hash == "0x123"
    assert transaction.price_eth == 1.0

def test_trait_rarity_calculation():
    """Test trait rarity score calculation."""
    trait = Trait.from_api_response(
        trait_type="Background",
        value="Blue",
        count=100,
        total_supply=1000
    )
    assert trait.rarity_score == 10.0  # 1/(100/1000)
