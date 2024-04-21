def list_of(list_of_data, trans_block, element):
    """
    :param list_of_data: A variable that contains a list of transaction blocks.
    :param trans_block: The key indicating the transaction block number.
    :param element: The key indicating the element to be printed from the asset_events list.

    :return: list of values for the given element
    """
    list_of_values = []
    for i in range(0, len(list_of_data[trans_block]['asset_events'])):
        list_of_values.append(list_of_data[trans_block]['asset_events'][i][element])

    return list_of_values


# %%
def myenumerator(x, column):
    """
    :param x: list, the input list or dataframe
    :param column: int or str, the column index or name to be enumerated
    :return: None

    Enumerates the elements in the specified column of the input list or dataframe.
    The function iterates over the elements in the specified column of the input list or dataframe using the enumerate() function.
    Each element is assigned a unique index starting from 0. The function then prints the index and the corresponding element.

    Example Usage:
    --------------
    >>> x = {'A': [10, 20, 30], 'B': [40, 50, 60]}
    >>> column = 'A'
    >>> myenumerator(x, column)
    Entry n: 0 , 10
    Entry n: 1 , 20
    Entry n: 2 , 30

    Note:
    -----
    - The input column can be specified either as an index or a column name.
    - The function does not return any value, it only prints the enumerated entries.

    """
    for index, transaction in enumerate(x[column]):
        print(f'Entry n: {index} , {transaction} \n')


# %%
def extract_and_print_keys_from_dict(d: dict):
    """
    Extracts and prints all keys from a nested dictionary.

    :param d: The dictionary to extract keys from.
    :type d: dict
    :return: None
    """

    def extract_keys(d, parent_key=''):
        keys = []
        for k, v in d.items():
            new_key = f"{parent_key}.{k}" if parent_key else k
            keys.append(new_key)
            if isinstance(v, dict):
                keys.extend(extract_keys(v, new_key))
        return keys

    keys = extract_keys(d)

    # Printing the keys
    for key in keys:
        print(key)

#%%
def how_long(file_data):
    """
    Calculate the total number of asset events in the given file_data.

    :param file_data: The data containing the asset events.
    :return: The total number of asset events in the file_data.

    """
    event_count = sum(len(block['asset_events']) for block in file_data)
    return event_count
#%%
