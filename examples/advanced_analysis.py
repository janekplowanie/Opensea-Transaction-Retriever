from opensea_transaction_retriever import OpenSeaClient
from opensea_transaction_retriever.visualization import (
    plot_trait_distribution,
    plot_rarity_scores,
    plot_trait_correlation
)

def analyze_collection_traits(client: OpenSeaClient, collection_slug: str):
    """Perform detailed trait analysis for a collection."""
    
    # Get collection data and calculate rarity
    collection = client.get_collection(collection_slug)
    trait_rarity = client.calculate_collection_rarity(collection_slug)

    # Plot trait distributions and rarity scores
    for trait_type in trait_rarity.keys():
        plot_trait_distribution(trait_rarity, trait_type)
        plot_rarity_scores(trait_rarity, trait_type)

def main():
    client = OpenSeaClient()
    collection_slug = "boredapeyachtclub"

    # Analyze traits
    analyze_collection_traits(client, collection_slug)

    # Get transactions with trait data
    transactions = client.get_collection_transactions(
        collection_slug=collection_slug,
        t_before="2024-01-01 00:00:00",
        t_after="2023-12-01 00:00:00"
    )

    # Plot trait-price correlations
    plot_trait_correlation(
        [t.__dict__ for t in transactions],
        trait_type="Background"
    )

if __name__ == "__main__":
    main()
