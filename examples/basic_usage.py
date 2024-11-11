from opensea_transaction_retriever import OpenSeaClient
from datetime import datetime, timedelta

def main():
    # Initialize client
    client = OpenSeaClient()  # Assumes API_KEY is in environment variables

    # Set time range for last 7 days
    end_time = datetime.now()
    start_time = end_time - timedelta(days=7)
    
    # Format times for API
    t_before = end_time.strftime('%Y-%m-%d %H:%M:%S')
    t_after = start_time.strftime('%Y-%m-%d %H:%M:%S')

    # Fetch transactions for a collection
    collection_slug = "boredapeyachtclub"
    transactions = client.get_collection_transactions(
        collection_slug=collection_slug,
        t_before=t_before,
        t_after=t_after,
        save_to_file="bayc_transactions.json"
    )

    # Plot basic analytics
    from opensea_transaction_retriever.visualization import (
        plot_price_history,
        plot_volume_over_time
    )

    plot_price_history(transactions, title="BAYC Price History")
    plot_volume_over_time(transactions, title="BAYC Trading Volume")

if __name__ == "__main__":
    main()
