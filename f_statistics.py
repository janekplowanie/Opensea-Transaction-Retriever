import pandas as pd

def correlation_by_decile(df, column_deciles:str, column_correlations:str):
    """
    Calculates the correlation between rarity_score and percentage_return for each decile of rarity_score.

    Args:
        df (pandas.DataFrame): The DataFrame containing the data.

    Returns:
        pandas.Series: A Series containing the correlation coefficients for each decile.
    """
    # Discretize rarity_score into deciles
    deciles = pd.qcut(df[column_deciles], 10, labels=range(1, 11))

    # Group by deciles and calculate correlation
    correlation_by_decile = df.groupby(deciles)[column_deciles, column_correlations].corr(method='spearman')

    # Extract correlation for 'rarity_score' - 'percentage_return'
    return correlation_by_decile[column_deciles][column_correlations]

#%%
