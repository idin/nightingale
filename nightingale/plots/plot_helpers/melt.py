import pandas as pd
from typing import Union, List, Optional

def melt(df: pd.DataFrame, columns: Union[List[str], str], group_column: Optional[str] = 'group', value_column: Optional[str] = 'value') -> pd.DataFrame:
    """
    Converts a wide DataFrame into a long format by melting specified columns.
    
    Parameters:
        df (pd.DataFrame): Input DataFrame.
        columns (Union[List[str], str]): Columns to be melted.
        group_column (Optional[str]): Name of the new column containing the original column names.
        value_column (Optional[str]): Name of the new column containing the values.

    Returns:
        pd.DataFrame: Melted DataFrame with specified group and value columns.
    """
    if isinstance(columns, str):
        columns = [columns]

    if group_column in df.columns:
        raise ValueError(f"group_column {group_column} is already a column in the dataframe with columns: {df.columns.tolist()}")

    if value_column in df.columns:
        raise ValueError(f"value_column {value_column} is already a column in the dataframe with columns: {df.columns.tolist()}")


    # Preserve all other columns as id_vars
    id_vars = [col for col in df.columns if col not in columns]

    # Melt the dataframe
    df_melted = df.melt(id_vars=id_vars, value_vars=columns, var_name=group_column, value_name=value_column)
    return df_melted
