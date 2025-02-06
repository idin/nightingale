from typing import Dict, Any, Optional, Union, List, Tuple
from .melt import melt
import pandas as pd
import numpy as np


def has_name(l):
    try:
        return l.name is not None
    except:
        return False



def convert_list_of_collections_to_df(
        list_of_collections: List[Union[pd.Series, np.ndarray, list]], 
        value_column_name: Optional[str] = 'value', group_column_name: Optional[str] = 'group',
        group_names: Optional[Union[str, List[str]]] = None
    ) -> pd.DataFrame:
    
    # group_names aren't provided, we either use group_column_name or if the collections have names we use them
    if group_names is None:
        if all(has_name(l) for l in list_of_collections):
            group_names = [l.name for l in list_of_collections]
        else:
            group_names = group_column_name

    # if group_names is a string, we make it a list
    if isinstance(group_names, str):
        group_names = [f'{group_names}_{i}' for i in range(len(list_of_collections))]

    if not len(list_of_collections) == len(group_names):
        raise ValueError(f'list_of_collections and group_names must have the same length, but they have lengths {len(list_of_collections)} and {len(group_names)}')

    # put all the collections under each other in the same column, with group names as indicators
    df_list = []
    for group_name, collection in zip(group_names, list_of_collections):
        df = pd.DataFrame()
        df[value_column_name] = collection
        df[group_column_name] = group_name
        df_list.append(df)

    df = pd.concat(df_list)
    # return what is necessary
    return {
        'df': df,
        'value_column_name': value_column_name,
        'group_column_name': group_column_name,
        'group_names': group_names
    }


def convert_dict_of_collections_to_df(
        dict_of_collections: Dict[str, Union[pd.Series, np.ndarray, list]], 
        value_column_name: Optional[str] = 'value', group_column_name: Optional[str] = 'group',
        group_names: Optional[Union[str, List[str]]] = None
    ) -> pd.DataFrame:

    # if group_names aren't provided, we use the keys of the dictionary
    if group_names is None:
        group_names = list(dict_of_collections.keys())

    return convert_list_of_collections_to_df(
        list_of_collections=list(dict_of_collections.values()), value_column_name=value_column_name, group_column_name=group_column_name, group_names=group_names
    )

def convert_list_or_dict_of_collections_to_df(
        list_or_dict_of_collections: Union[List[Union[pd.Series, np.ndarray, list]], Dict[str, Union[pd.Series, np.ndarray, list]]],
        value_column_name: Optional[str] = 'value', group_column_name: Optional[str] = 'group',
        group_names: Optional[Union[str, List[str]]] = None
) -> pd.DataFrame:
    if isinstance(list_or_dict_of_collections, dict):
        return convert_dict_of_collections_to_df(
            dict_of_collections=list_or_dict_of_collections, value_column_name=value_column_name, group_column_name=group_column_name, group_names=group_names
        )
    elif isinstance(list_or_dict_of_collections, list):
        return convert_list_of_collections_to_df(
            list_of_collections=list_or_dict_of_collections, value_column_name=value_column_name, group_column_name=group_column_name, group_names=group_names
        )


def convert_collection_to_df(
        collection: Union[pd.Series, np.ndarray, list],
        value_column_name: Optional[str] = 'value'
) -> pd.DataFrame:

    df = pd.DataFrame({value_column_name: collection})
    return {
        'df': df,
        'value_column_name': value_column_name
    }


def convert_two_collections_to_df(
        x: Union[pd.Series, np.ndarray, list],
        y: Union[pd.Series, np.ndarray, list],
        x_column_name: Optional[str] = 'x',
        y_column_name: Optional[str] = 'y'
) -> pd.DataFrame:

    # length of x and y should be the same
    if not len(x) == len(y):
        raise ValueError(f'x and y must have the same length, but they have lengths {len(x)} and {len(y)}')

    # put x and y under each other in the same column, with group names as indicators
    df = pd.DataFrame({x_column_name: x, y_column_name: y})
    return {
        'df': df,
        'x_column_name': x_column_name,
        'y_column_name': y_column_name
    }


def convert_list_of_collections_and_a_collection_to_df(
        list_of_collections: List[Union[pd.Series, np.ndarray, list]],
        collection: Union[pd.Series, np.ndarray, list],
        list_of_collections_value_column_name: Optional[str] = 'x',
        collection_value_column_name: Optional[str] = 'y',
        group_column_name: Optional[str] = 'group',
        group_names: Optional[Union[str, List[str]]] = None
) -> pd.DataFrame:
    

    # length of collection should be the same as every element of list_of_collections
    for x_collection in list_of_collections:
        if not len(x_collection) == len(collection):
            raise ValueError(f'collection and list_of_collections must have the same length, but they have lengths {len(collection)} and {len(x_collection)}')

    if group_names is None:
        if all(has_name(l) for l in list_of_collections):
            group_names = [l.name for l in list_of_collections]
        else:
            group_names = group_column_name

    if isinstance(group_names, str):
        group_names = [f'{group_names}_{i}' for i in range(len(list_of_collections))]

    if not len(list_of_collections) == len(group_names):
        raise ValueError(f'list_of_collections and group_names must have the same length, but they have lengths {len(list_of_collections)} and {len(group_names)}')

    df_list = []
    for group_name, x_collection in zip(group_names, list_of_collections):
        df = pd.DataFrame()
        df[list_of_collections_value_column_name] = x_collection
        df[group_column_name] = group_name

        df[collection_value_column_name] = collection
        df_list.append(df)

    df = pd.concat(df_list)
    return {
        'df': df,
        'list_of_collections_value_column_name': list_of_collections_value_column_name,
        'collection_value_column_name': collection_value_column_name,
        'group_column_name': group_column_name,
        'group_names': group_names
    }

def convert_dict_of_collections_and_a_collection_to_df(
        dict_of_collections: Dict[str, Union[pd.Series, np.ndarray, list]],
        collection: Union[pd.Series, np.ndarray, list],
        dict_of_collections_value_column_name: Optional[str] = 'x',
        collection_value_column_name: Optional[str] = 'y',
        group_column_name: Optional[str] = 'group',
        group_names: Optional[Union[str, List[str]]] = None
) -> pd.DataFrame:
    # if group_names aren't provided, we use the keys of the dictionary
    if group_names is None:
        group_names = list(dict_of_collections.keys())

    return convert_list_of_collections_and_a_collection_to_df(
        list_of_collections=list(dict_of_collections.values()),
        collection=collection,
        list_of_collections_value_column_name=dict_of_collections_value_column_name,
        collection_value_column_name=collection_value_column_name,
        group_column_name=group_column_name,
        group_names=group_names
    )

def convert_list_or_dict_of_collections_and_a_collection_to_df(
        list_or_dict_of_collections: Union[List[Union[pd.Series, np.ndarray, list]], Dict[str, Union[pd.Series, np.ndarray, list]]],
        collection: Union[pd.Series, np.ndarray, list],
        list_or_dict_of_collections_value_column_name: Optional[str] = 'x',
        collection_value_column_name: Optional[str] = 'y',
        group_column_name: Optional[str] = 'group',
        group_names: Optional[Union[str, List[str]]] = None
) -> pd.DataFrame:
    if isinstance(list_or_dict_of_collections, dict):
        return convert_dict_of_collections_and_a_collection_to_df(
            dict_of_collections=list_or_dict_of_collections,
            collection=collection,
            dict_of_collections_value_column_name=list_or_dict_of_collections_value_column_name,
            collection_value_column_name=collection_value_column_name,
            group_column_name=group_column_name,
            group_names=group_names
        )
    elif isinstance(list_or_dict_of_collections, list):
        return convert_list_of_collections_and_a_collection_to_df(
            list_of_collections=list_or_dict_of_collections,
            collection=collection,
            list_of_collections_value_column_name=list_or_dict_of_collections_value_column_name,
            collection_value_column_name=collection_value_column_name,
            group_column_name=group_column_name,
            group_names=group_names
        )


def convert_df_and_list_of_columns_to_df(
        df: pd.DataFrame,
        column_names: List[str],
        value_column_name: Optional[str] = 'value',
        group_column_name: Optional[str] = 'group'
) -> pd.DataFrame:

    # column_names should be a subset of the columns of df
    for column_name in column_names:
        if column_name not in df.columns:
            raise ValueError(f'column_name {column_name} is not a column of df')

    df = melt(df=df, columns=column_names, group_column=group_column_name, value_column=value_column_name)
    return {
        'df': df,
        'value_column_name': value_column_name,
        'group_column_name': group_column_name
    }

