from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List, Dict, Any

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

    @property
    def datetime(self) -> datetime:
        """Convert Unix timestamp to datetime object."""
        return datetime.fromtimestamp(self.event_timestamp)

    @property
    def price_eth(self) -> float:
        """Get price in ETH, considering token decimals."""
        decimals = self.payment_token.get('decimals', 18)
        return self.total_price / (10 ** decimals)

    @classmethod
    def from_api_response(cls, data: Dict[str, Any]) -> 'Transaction':
        """Create Transaction instance from OpenSea API response."""
        return cls(
            transaction_hash=data.get('transaction_hash'),
            event_timestamp=data.get('event_timestamp'),
            total_price=float(data.get('total_price', 0)),
            payment_token=data.get('payment_token', {}),
            seller_address=data.get('seller', {}).get('address'),
            buyer_address=data.get('buyer', {}).get('address'),
            collection_slug=data.get('collection', {}).get('slug'),
            nft_id=data.get('nft', {}).get('identifier'),
            nft_metadata_url=data.get('nft', {}).get('metadata_url'),
            nft_traits=data.get('nft', {}).get('traits')
        )
