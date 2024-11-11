import matplotlib.pyplot as plt
from typing import Dict, List, Optional
import pandas as pd
from ..models.trait import Trait

def plot_trait_distribution(traits: Dict[str, List[Trait]],
                          trait_type: str,
                          title: Optional[str] = None,
                          save_path: Optional[str] = None):
    """Plot distribution of trait values for a specific trait type."""
    if trait_type not in traits:
        raise ValueError(f"Trait type '{trait_type}' not found")
    
    trait_data = traits[trait_type]
    values = [t.value for t in trait_data]
    counts = [t.count for t in trait_data]
    
    plt.figure(figsize=(12, 6))
    plt.bar(values, counts, alpha=0.7)
    plt.title(title or f'Distribution of {trait_type}')
    plt.xlabel('Trait Value')
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    plt.grid(True, alpha=0.3)
    
    if save_path:
        plt.savefig(save_path)
    plt.show()

def plot_rarity_scores(traits: Dict[str, List[Trait]],
                      trait_type: str,
                      title: Optional[str] = None,
                      save_path: Optional[str] = None):
    """Plot rarity scores for a specific trait type."""
    if trait_type not in traits:
        raise ValueError(f"Trait type '{trait_type}' not found")
    
    trait_data = traits[trait_type]
    values = [t.value for t in trait_data]
    rarity_scores = [t.rarity_score for t in trait_data]
    
    plt.figure(figsize=(12, 6))
    plt.bar(values, rarity_scores, alpha=0.7)
    plt.title(title or f'Rarity Scores for {trait_type}')
    plt.xlabel('Trait Value')
    plt.ylabel('Rarity Score')
    plt.xticks(rotation=45)
    plt.grid(True, alpha=0.3)
    
    if save_path:
        plt.savefig(save_path)
    plt.show()

def plot_trait_correlation(transactions: List[Dict],
                         trait_type: str,
                         title: Optional[str] = None,
                         save_path: Optional[str] = None):
    """Plot correlation between trait rarity and price."""
    df = pd.DataFrame(transactions)
    trait_scores = df.groupby('nft_id').apply(
        lambda x: x['rarity_score'].mean() if 'rarity_score' in x else 0
    )
    prices = df.groupby('nft_id')['price_eth'].mean()
    
    plt.figure(figsize=(10, 6))
    plt.scatter(trait_scores, prices, alpha=0.5)
    plt.title(title or f'Price vs Rarity Score for {trait_type}')
    plt.xlabel('Rarity Score')
    plt.ylabel('Price (ETH)')
    plt.grid(True, alpha=0.3)
    
    if save_path:
        plt.savefig(save_path)
    plt.show()
