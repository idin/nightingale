import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from typing import Optional, Union, Dict
from .plot_helpers import infer_plot_arguments
from .plot_helpers import get_plot_kwargs


def line_plot(
        x: Union[pd.Series, np.ndarray, list, str],
        y: Union[pd.Series, np.ndarray, list, str],
        df: Optional[pd.DataFrame] = None,
        colour_by: Optional[Union[pd.Series, np.ndarray, list, str]] = None,
        line_type_by: Optional[Union[pd.Series, np.ndarray, list, str]] = None,
        colours: Optional[Union[str, list, Dict[str, str]]] = None,
        line_types: Optional[Union[str, list, Dict[str, str]]] = None,
        line_opacity: Optional[float] = 1,
        title: Optional[str] = None,
        x_label: Optional[str] = None,
        y_label: Optional[str] = None,
        colour_label: Optional[str] = None,
        line_type_label: Optional[str] = None,
        x_range: Optional[Union[list, tuple]] = None,
        y_range: Optional[Union[list, tuple]] = None,
        line_width: Optional[float] = 2,
        display: Optional[bool] = False,
        width: Optional[int] = None,
        height: Optional[int] = None,
        sort_by_x: Optional[bool] = True,
        sort_by_y: Optional[bool] = False
) -> Union[go.Figure, None]:
    """
    Create a line plot.

    Args:
        x (Union[pd.Series, np.ndarray, list, str]): Data for the x-axis. It can be a single column name, a list of column names, a pandas Series, a numpy array, a list of numbers, or a list of lists of numbers, list of pandas Series or list of numpy arrays.
        y (Union[pd.Series, np.ndarray, list, str]): Data for the y-axis. It can be a single column name, a list of column names, a pandas Series, a numpy array, a list of numbers, or a list of lists of numbers, list of pandas Series or list of numpy arrays.
        df (Optional[pd.DataFrame]): DataFrame containing the data. It should only be provided if x and y are column names or lists of column names.
        colour_by (Optional[Union[pd.Series, np.ndarray, list, str]]): Column to color the lines by. If not provided, the default color will be used.
        line_type_by (Optional[Union[pd.Series, np.ndarray, list, str]]): Column to differentiate line types. If not provided, a single line will be drawn.
        
        colours (Optional[Union[str, list, Dict[str, str]]]): Colors to use for the lines. If provided, it will override the default colors.
        line_types (Optional[Union[str, list, Dict[str, str]]]): Line types to use. If provided, it will override the default line types.
        line_opacity (Optional[float]): Opacity of the lines. Default is 1 (fully opaque).
        
        title (Optional[str]): Title of the plot.
        x_label (Optional[str]): Label for the x-axis. If not provided, it will be inferred from x.
        y_label (Optional[str]): Label for the y-axis. If not provided, it will be inferred from y.
        colour_label (Optional[str]): Label for the color legend. If not provided, it will be inferred from colour_by.
        line_type_label (Optional[str]): Label for the line type legend. If not provided, it will be inferred from line_type_by.
        
        x_range (Optional[Union[list, tuple]]): Range for the x-axis.
        y_range (Optional[Union[list, tuple]]): Range for the y-axis.
        line_width (Optional[float]): Width of the lines. Default is 2.
        
        display (Optional[bool]): Whether to display the plot. If True, the plot will be displayed and the function will return None. Otherwise, a figure will be returned which can be displayed by the .show() method.
        width (Optional[int]): Width of the plot. If provided, it will override the default width.
        height (Optional[int]): Height of the plot. If provided, it will override the default height.
        
        sort_by_x (Optional[bool]): Whether to sort by x values. Default is True.
        sort_by_y (Optional[bool]): Whether to sort by y values. Default is False.

    Returns:
        plotly.graph_objects.Figure: The line plot figure. If display is True, the plot will be displayed and the function will return None. Otherwise, a figure will be returned which can be displayed by the .show() method.
    """
    # make sure x and y are the same length if they are not strings
    
    kwargs = infer_plot_arguments(
        x=x,
        y=y,
        df=df,
        colour_by=colour_by
    )

    x = kwargs['x']
    y = kwargs['y']
    df = kwargs['df']
    colour_by = kwargs['colour_by']

    # if sort_by_x, sort the dataframe which is plot_kwargs['data_frame'] by the x column which is plot_kwargs['x']
    if sort_by_x and not sort_by_y:
        df = df.sort_values(by=x)

    elif sort_by_y and not sort_by_x:
        df = df.sort_values(by=y)

    elif sort_by_x and sort_by_y:
        raise ValueError('sort_by_x and sort_by_y cannot both be True')
    
    all_kwargs = get_plot_kwargs(
        x=x,
        y=y,
        df=df,
        colour_by=colour_by,
        line_type_by=line_type_by, 
        colours=colours,
        line_types=line_types,
        title=title,
        x_label=x_label,
        y_label=y_label, 
        width=width,
        height=height,
        line_width=line_width,
        line_opacity=line_opacity,
        x_range=x_range,
        y_range=y_range, 
        line_type_label=line_type_label,
        colour_label=colour_label

    )

    plot_kwargs = all_kwargs['plot_kwargs']
    update_traces_kwargs = all_kwargs['update_traces_kwargs']
    update_layout_kwargs = all_kwargs['update_layout_kwargs']

    fig = px.line(**plot_kwargs)
    fig.update_traces(**update_traces_kwargs)
    fig.update_layout(**update_layout_kwargs)

    if display:
        fig.show()

        return None

    return fig
