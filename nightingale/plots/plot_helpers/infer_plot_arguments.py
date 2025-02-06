from .convert_collections_to_df import convert_list_of_collections_to_df, convert_dict_of_collections_to_df
from .convert_collections_to_df import convert_collection_to_df, convert_two_collections_to_df, convert_df_and_list_of_columns_to_df
from .convert_collections_to_df import convert_list_or_dict_of_collections_to_df, convert_list_or_dict_of_collections_and_a_collection_to_df
import pandas as pd
import numpy as np
from typing import Optional, Union, Dict, Any

def is_collection(x):
    return isinstance(x, (pd.Series, np.ndarray, dict, list))

def is_list_or_dict_of_collections(x):
    if isinstance(x, dict):
        return all(is_collection(i) for i in x.values())
    elif isinstance(x, list):
        return all(is_collection(i) for i in x)
    else:
        return False

def is_a_simple_collection(x):
    return is_collection(x) and not is_list_or_dict_of_collections(x)

def infer_plot_arguments(
        df: Optional[pd.DataFrame] = None,

        x: Optional[Union[pd.Series, np.ndarray, dict, list, str]] = None,
        y: Optional[Union[pd.Series, np.ndarray, dict, list, str]] = None,
        colour_by: Optional[str] = None
) -> Dict[str, Any]:
    
    if isinstance(df, pd.DataFrame):
        if x is None and y is None:
            raise ValueError('x and y cannot both be None')
        assert x is None or isinstance(x, str) or is_collection(x), f'x must be a string or a collection, but it is a {type(x)}'
        assert y is None or isinstance(y, str) or is_collection(y), f'y must be a string or a collection, but it is a {type(y)}'

        if y is None or isinstance(y, str):
            if isinstance(x, str):
                return {
                    'df': df,
                    'x': x,
                    'y': y,
                    'colour_by': colour_by
                }
            elif isinstance(x, list) and all(isinstance(item, str) for item in x):
                arguments = convert_df_and_list_of_columns_to_df(
                    df=df,
                    column_names=x,
                    value_column_name='x',
                    group_column_name=colour_by or 'group'
                )
                df = arguments['df']
                x = arguments['value_column_name']
                colour_by = arguments['group_column_name']
                return {
                    'df': df,
                    'x': x,
                    'y': y,
                    'colour_by': colour_by
                }
            else:
                raise TypeError(f'x: {x} is neither a string nor a list of strings')
        elif x is None or isinstance(x, str):
            if isinstance(y, str):
                return {
                    'df': df,
                    'x': x,
                    'y': y,
                    'colour_by': colour_by
                }
            elif isinstance(y, list) and all(isinstance(item, str) for item in y):
                arguments = convert_df_and_list_of_columns_to_df(
                    df=df,
                    column_names=y,
                    value_column_name='y',
                    group_column_name=colour_by or 'group'
                )
                df = arguments['df']

                y = arguments['value_column_name']
                colour_by = arguments['group_column_name']
                return {
                    'df': df,
                    'x': x,
                    'y': y,
                    'colour_by': colour_by
                }
            else:
                raise TypeError(f'y: {y} is neither a string nor a list of strings')

        else:
            raise TypeError(f'x: {x} of type {type(x)} and y: {y} of type {type(y)} are not compatible.')


    # x and y are collections
    if is_collection(x) or is_collection(y):
        if df is not None:
            raise ValueError('df cannot be provided if x or y are collections')
        
        if y is None:
            if is_a_simple_collection(x):
                arguments = convert_collection_to_df(collection=x, value_column_name='x')
                df = arguments['df']
                x = arguments['value_column_name']
            elif is_list_or_dict_of_collections(x):
                arguments = convert_list_or_dict_of_collections_to_df(
                    list_or_dict_of_collections=x, value_column_name='x', 
                    group_column_name=colour_by or 'group'
                )
                df = arguments['df']
                x = arguments['value_column_name']
                _ = arguments['group_names']
                colour_by = arguments['group_column_name']

            else:
                raise TypeError(f'x: {x} is neither a collection nor a list or dictionary of collections')

        elif x is None:
            if is_a_simple_collection(y):
                arguments = convert_collection_to_df(collection=y, value_column_name='y')
                df = arguments['df']
                y = arguments['value_column_name']
            elif is_list_or_dict_of_collections(y):
                arguments = convert_list_or_dict_of_collections_to_df(
                    list_or_dict_of_collections=y, value_column_name='y',
                    group_column_name=colour_by or 'group'
                )
                df = arguments['df']
                y = arguments['value_column_name']
                _ = arguments['group_names']
                colour_by = arguments['group_column_name']


            else:
                raise TypeError(f'y: {y} is neither a collection nor a list or dictionary of collections')

        else:
            # both x and y exist
            if is_list_or_dict_of_collections(x) and is_a_simple_collection(y):
                arguments = convert_list_or_dict_of_collections_and_a_collection_to_df(
                    list_or_dict_of_collections=x, 
                    list_or_dict_of_collections_value_column_name='x', 
                    collection=y, 
                    collection_value_column_name='y',
                    group_column_name=colour_by or 'group'
                )
                df = arguments['df']
                x = arguments['list_of_collections_value_column_name']
                y = arguments['collection_value_column_name']
                _ = arguments['group_names']
                colour_by = arguments['group_column_name']

            elif is_a_simple_collection(x) and is_list_or_dict_of_collections(y):
                arguments = convert_list_or_dict_of_collections_and_a_collection_to_df(
                    list_or_dict_of_collections=y,
                    list_or_dict_of_collections_value_column_name='y',
                    collection=x,
                    collection_value_column_name='x',
                    group_column_name=colour_by or 'group'
                )
                df = arguments['df']
                x = arguments['collection_value_column_name']
                y = arguments['list_of_collections_value_column_name']
                _ = arguments['group_names']
                colour_by = arguments['group_column_name']

            elif is_a_simple_collection(x) and is_a_simple_collection(y):
                arguments = convert_two_collections_to_df(x=x, y=y, x_column_name='x', y_column_name='y')
                df = arguments['df']
                x = arguments['x_column_name']
                y = arguments['y_column_name']

            elif is_list_or_dict_of_collections(x) and is_list_or_dict_of_collections(y):
                raise TypeError('x and y cannot both be lists or dictionaries of collections')

            else:
                raise TypeError(f'x: {x} and y: {y} are neither collections nor lists or dictionaries of collections')

    return {
        'df': df,
        'x': x,
        'y': y,
        'colour_by': colour_by
    }
