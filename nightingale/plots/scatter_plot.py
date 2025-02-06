from .plot_helpers import get_plot_kwargs, infer_plot_arguments
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from typing import Optional, Union, Dict

def scatter_plot(
    x: Union[pd.Series, np.ndarray, list, str],
    y: Union[pd.Series, np.ndarray, list, str],
    df: Optional[pd.DataFrame] = None,
    title: Optional[str] = None,
    x_label: Optional[str] = None,
    y_label: Optional[str] = None,
    colour_by: Optional[Union[pd.Series, np.ndarray, list, str]] = None,
    colour_label: Optional[str] = None,
    colours: Optional[Union[str, list, Dict[str, str]]] = None,
    size_by: Optional[Union[pd.Series, np.ndarray, list, str]] = None,
    size_label: Optional[str] = None,
    size_max: Optional[float] = None,
    # size_min: Optional[float] = None,
    display: Optional[bool] = False,
    width: Optional[int] = None,
    height: Optional[int] = None
) -> Union[go.Figure, None]:
    """
    Create a scatter plot.


    Args:
        x (Union[pd.Series, np.ndarray, list, str]): Data for the x-axis. It can be a single column name, a list of column names, a pandas Series, a numpy array, a list of numbers, or a list of lists of numbers, list of pandas Series or list of numpy arrays.
        y (Union[pd.Series, np.ndarray, list, str]): Data for the y-axis. It can be a single column name, a list of column names, a pandas Series, a numpy array, a list of numbers, or a list of lists of numbers, list of pandas Series or list of numpy arrays.
        df (Optional[pd.DataFrame]): DataFrame containing the data. It should only be provided if x and y are column names or lists of column names.
        title (Optional[str]): Title of the plot.

        x_label (Optional[str]): Label for the x-axis. If not provided, it will be inferred from x.
        y_label (Optional[str]): Label for the y-axis. If not provided, it will be inferred from y.
        colour_by (Optional[Union[pd.Series, np.ndarray, list, str]]): Column to colour the points by. If not provided but x or y indicate multiple columns, the data will be melted and colour_by will be set to the group column.
        colour_label (Optional[str]): Label for the color legend. If not provided, it will be inferred from colour_by.

        colours (Optional[Union[str, list, Dict[str, str]]]): Colors to use for the points. If provided, it will override the default colours.
        size_by (Optional[Union[pd.Series, np.ndarray, list, str]]): Column to size the points by. 
        size_label (Optional[str]): Label for the size legend. If not provided, it will be inferred from size_by.
        size_max (Optional[float]): Maximum size of the points. If provided, it will normalize the size of the points to the range [0, size_max].
        display (Optional[bool]): Whether to display the plot. If True, the plot will be displayed and the function will return None. Otherwise a figure will be returned which can be displayed by the .show() method.
        width (Optional[int]): Width of the plot. If provided, it will override the default width.
        height (Optional[int]): Height of the plot. If provided, it will override the default height.

    Returns:
        Union[plotly.graph_objects.Figure, None]: The scatter plot figure. If display is True, the plot will be displayed and the function will return None. Otherwise a figure will be returned which can be displayed by the .show() method.
    """


    inferred_kwargs = infer_plot_arguments(
        x=x,
        y=y,
        df=df,
        colour_by=colour_by
    )
    x = inferred_kwargs['x']
    y = inferred_kwargs['y']
    df = inferred_kwargs['df']
    colour_by = inferred_kwargs['colour_by']
    del inferred_kwargs

    kwargs = get_plot_kwargs(
        x=x,
        y=y,
        df=df,
        title=title,
        x_label=x_label,
        y_label=y_label,
        colour_by=colour_by,
        colour_label=colour_label,
        colours=colours,
        size_by=size_by,
        size_label=size_label,
        size_max=size_max,
        #size_min=size_min,
        width=width,
        height=height
    )

    plot_kwargs = kwargs['plot_kwargs']
    update_traces_kwargs = kwargs['update_traces_kwargs']
    update_layout_kwargs = kwargs['update_layout_kwargs']

    # make sure the columns of df are unique
    df = plot_kwargs['data_frame']
    column_names = df.columns.tolist()
    if len(column_names) != len(set(column_names)):
        raise ValueError("The columns of df must be unique.")

    fig = px.scatter(**plot_kwargs)
    fig.update_traces(**update_traces_kwargs)
    fig.update_layout(**update_layout_kwargs)

    if display:
        fig.show()
        return None

    return fig
