import os
import time
import calendar
from typing import List, Dict, Optional, Any
import requests
from tenacity import retry, wait_exponential
from dotenv import load_dotenv

from .models.transaction import Transaction
from .models.collection import Collection
from .utils.data_utils import calculate_trait_rarity, save_json
from .utils.time_utils import format_datetime

class OpenSeaClient:
    """Client for interacting with the OpenSea API."""
    
    def __init__(self, api_key: str = None):
        """Initialize OpenSea client with API key."""
        self.api_key = api_key or os.getenv("API_KEY")
        if not self.api_key:
            raise ValueError("No API_KEY provided or found in environment variables.")
        
        self.session = requests.Session()
        self.headers = {
            "accept": "application/json",
            "x-api-key": self.api_key
        }
        self.base_url = "https://api.opensea.io/api/v2"

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()

    @retry(wait=wait_exponential(multiplier=2, min=1, max=10))
    def _make_request(self, endpoint: str, params: Optional[Dict] = None) -> Dict:
        """Make API request with retry logic."""
        url = f"{self.base_url}/{endpoint}"
        response = self.session.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()

    def get_collection_transactions(self, 
                                  collection_slug: str, 
                                  t_before: str, 
                                  t_after: str, 
                                  event_type: str = "successful",
                                  save_to_file: Optional[str] = None) -> List[Transaction]:
        """
        Fetch all transactions for a collection within a time range.
        
        Args:
            collection_slug: Collection identifier
            t_before: End time (format: 'YYYY-MM-DD HH:MM:SS')
            t_after: Start time (format: 'YYYY-MM-DD HH:MM:SS')
            event_type: Type of event to fetch
            save_to_file: Optional file path to save raw response
        """
        t_after_unix = calendar.timegm(time.strptime(t_after, '%Y-%m-%d %H:%M:%S'))
        t_before_unix = calendar.timegm(time.strptime(t_before, '%Y-%m-%d %H:%M:%S'))
        
        params = {
            "after": t_after_unix,
            "before": t_before_unix,
            "event_type": event_type
        }
        
        all_transactions = []
        start_time = time.time()

        try:
            while True:
                response = self._make_request(f"events/collection/{collection_slug}", params)
                events = response.get('asset_events', [])
                all_transactions.extend([Transaction.from_api_response(event) for event in events])

                if 'next' in response and response['next']:
                    params['next'] = response['next']
                else:
                    break

        finally:
            elapsed_time = (time.time() - start_time) / 60
            print(f'Fetched {len(all_transactions)} transactions in {elapsed_time:.2f} minutes')

        if save_to_file:
            save_json([t.__dict__ for t in all_transactions], save_to_file)

        return all_transactions

    def get_collection(self, collection_slug: str) -> Collection:
        """Fetch collection metadata."""
        response = self._make_request(f"collections/{collection_slug}")
        return Collection.from_api_response(response)

    def get_collection_traits(self, collection_slug: str) -> Dict[str, List[Dict]]:
        """Fetch trait statistics for a collection."""
        response = self._make_request(f"collections/{collection_slug}/traits")
        return response.get('traits', {})

    def get_nft_traits(self, collection_slug: str, token_id: str) -> List[Dict]:
        """Fetch traits for a specific NFT."""
        response = self._make_request(f"collections/{collection_slug}/nfts/{token_id}")
        return response.get('nft', {}).get('traits', [])

    def calculate_collection_rarity(self, collection_slug: str) -> Dict[str, List[Dict]]:
        """Calculate rarity scores for all traits in a collection."""
        collection = self.get_collection(collection_slug)
        traits_data = self.get_collection_traits(collection_slug)
        
        return calculate_trait_rarity(traits_data, collection.total_supply)
