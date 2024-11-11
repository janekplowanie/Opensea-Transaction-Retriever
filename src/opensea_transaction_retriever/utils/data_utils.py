import json
from typing import Dict, List, Any, Union
import pandas as pd
from ..models.transaction import Transaction
from ..models.trait import Trait

def load_json(file_path: str) -> Union[Dict, List]:
    """Load data from JSON file."""
    with open(file_path, 'r') as f:
        return json.load(f)

def save_json(data: Union[Dict, List], file_path: str) -> None:
    """Save data to JSON file."""
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)

def calculate_trait_rarity(traits_data: Dict[str, Dict[str, int]], 
                         total_supply: int) -> Dict[str, List[Trait]]:
    """
    Calculate rarity scores for traits.
    
    Args:
        traits_data: Dictionary of trait types and their value counts
        total_supply: Total number of NFTs in collection
    
    Returns:
        Dictionary of trait types with their Trait objects including rarity scores
    """
    trait_objects = {}
    for trait_type, values in traits_data.items():
        trait_objects[trait_type] = [
            Trait.from_api_response(
                trait_type=trait_type,
                value=value,
                count=count,
                total_supply=total_supply
            )
            for value, count in values.items()
        ]
    return trait_objects

def transactions_to_dataframe(transactions: List[Transaction]) -> pd.DataFrame:
    """Convert list of Transaction objects to pandas DataFrame."""
    return pd.DataFrame([{
        'transaction_hash': t.transaction_hash,
        'datetime': t.datetime,
        'price_eth': t.price_eth,
        'seller_address': t.seller_address,
        'buyer_address': t.buyer_address,
        'collection_slug': t.collection_slug,
        'nft_id': t.nft_id,
        'rarity_score': t.rarity_score
    } for t in transactions])

def calculate_nft_rarity(nft_traits: List[Dict[str, Any]], 
                        collection_traits: Dict[str, List[Trait]]) -> float:
    """
    Calculate overall rarity score for an NFT based on its traits.
    
    Args:
        nft_traits: List of trait dictionaries for the NFT
        collection_traits: Dictionary of trait types with their Trait objects
    
    Returns:
        Combined rarity score for the NFT
    """
    if not nft_traits or not collection_traits:
        return 0.0

    total_score = 0.0
    for trait in nft_traits:
        trait_type = trait.get('trait_type')
        trait_value = trait.get('value')
        
        if trait_type in collection_traits:
            matching_trait = next(
                (t for t in collection_traits[trait_type] 
                 if t.value == trait_value), 
                None
            )
            if matching_trait:
                total_score += matching_trait.rarity_score
                
    return total_score
