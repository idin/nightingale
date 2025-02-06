from ..distribution import probability_density_curve
from .plot_helpers import infer_plot_arguments
import pandas as pd
from typing import Optional, Union, Dict
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from .line_plot import line_plot

def density_plot(
    x: Union[pd.Series, np.ndarray, list, str],
    df: Optional[pd.DataFrame] = None,
    n: int = 100,
    colour_by: Optional[Union[pd.Series, np.ndarray, list, str]] = None,
    line_type_by: Optional[Union[pd.Series, np.ndarray, list, str]] = None,
    colours: Optional[Union[str, list, Dict[str, str]]] = None,
    line_types: Optional[Union[str, list, Dict[str, str]]] = None,
    line_opacity: Optional[float] = 1,
    title: Optional[str] = None,
    x_label: Optional[str] = None,
    y_label: Optional[str] = 'density',
    colour_label: Optional[str] = None,
    line_type_label: Optional[str] = None,
    x_range: Optional[Union[list, tuple]] = None,
    y_range: Optional[Union[list, tuple]] = None,
    line_width: Optional[float] = 2,
    display: Optional[bool] = False,
    width: Optional[int] = None,
    height: Optional[int] = None,
    separator: Optional[str] = '  ',
    bw_method: Optional[float] = 0.1
) -> Union[go.Figure, None]:
    """
    Create a density plot.


    Args:
        x (Union[pd.Series, np.ndarray, list, str]): Data for the x-axis. It can be a single column name, a list of column names, a pandas Series, a numpy array, a list of numbers, or a list of lists of numbers, list of pandas Series or list of numpy arrays
        df (Optional[pd.DataFrame]): DataFrame containing the data. It should only be provided if x is a column name or a list of column names.
        n (int): Number of points to generate for the density curve.
        colour_by (Optional[Union[pd.Series, np.ndarray, list, str]]): Column to color the density lines by. If not provided, the default color will be used.
        line_type_by (Optional[Union[pd.Series, np.ndarray, list, str]]): Column to differentiate line types. If not provided, a single line will be drawn.
        
        colours (Optional[Union[str, list, Dict[str, str]]]): Colors to use for the density lines. If provided, it will override the default colors.
        line_types (Optional[Union[str, list, Dict[str, str]]]): Line types to use. If provided, it will override the default line types.
        line_opacity (Optional[float]): Opacity of the density lines. Default is 1 (fully opaque).
    
        title (Optional[str]): Title of the plot.    
        x_label (Optional[str]): Label for the x-axis. If not provided, it will be inferred from x.
        y_label (Optional[str]): Label for the y-axis. Default is 'density'.
        colour_label (Optional[str]): Label for the color legend. If not provided, it will be inferred from colour_by.
        line_type_label (Optional[str]): Label for the line type legend. If not provided, it will be inferred from line_type_by.
        
        x_range (Optional[Union[list, tuple]]): Range for the x-axis.
        y_range (Optional[Union[list, tuple]]): Range for the y-axis.
        line_width (Optional[float]): Width of the density lines. Default is 2.
        
        display (Optional[bool]): Whether to display the plot. If True, the plot will be displayed and the function will return None. Otherwise, a figure will be returned which can be displayed by the .show() method.      
        width (Optional[int]): Width of the plot. If provided, it will override the default width.
        height (Optional[int]): Height of the plot. If provided, it will override the default height.
        separator (Optional[str]): Separator for grouping.
        bw_method (Optional[float]): Bandwidth method for density estimation.

    Returns:
        plotly.graph_objects.Figure: The density plot figure. If display is True, the plot will be displayed and the function will return None. Otherwise, a figure will be returned which can be displayed by the .show() method.
    """

    if isinstance(x, list):
        missing_columns = [col for col in x if col not in df.columns]
        existing_columns = [col for col in x if col in df.columns]
        if len(missing_columns) > 0:
            raise KeyError(f'columns {missing_columns} in x are not in df. Existing columns are: {existing_columns}. df has the following columns: {df.columns.tolist()}')

    inferred_kwargs = infer_plot_arguments(
        x=x,
        y=None,
        df=df,
        colour_by=colour_by
    )

    df = inferred_kwargs['df']
    x = inferred_kwargs['x']
    colour_by = inferred_kwargs['colour_by']
    del inferred_kwargs

    if isinstance(x, list):
        raise TypeError("x cannot be a list")

    """
    colours = plot_kwargs['colours']
    line_types = plot_kwargs['line_types']
    line_opacity = plot_kwargs['line_opacity']
    title = plot_kwargs['title']

    x_label = plot_kwargs['x_label']
    y_label = plot_kwargs['y_label']
    colour_label = plot_kwargs['colour_label']
    line_type_label = plot_kwargs['line_type_label']
    x_range = plot_kwargs['x_range']
    y_range = plot_kwargs['y_range']
    line_width = plot_kwargs['line_width']
    """

    if isinstance(x, str):
        x_label = x_label or x
    else:
        x_label = x_label or 'x'

    # it can be grouped by either by colour_by or line_type_by
    if colour_by is not None and line_type_by is None:
        group_by = colour_by
        grouped_by = 'colour'
    elif line_type_by is not None and colour_by is None:
        group_by = line_type_by
        grouped_by = 'line_type'
    elif colour_by is not None and line_type_by is not None:
        # we should put group_by together from both
        if isinstance(colour_by, str):
            colour_by = [colour_by]
        if isinstance(line_type_by, str):
            line_type_by = [line_type_by]
        group_by = list(colour_by) + list(line_type_by)
        grouped_by = 'colour_and_line_type'
    else:
        group_by = None
        grouped_by = None

    # Generate the density curve (either global or partial by group)
    density_curve = probability_density_curve(
        x=x,
        df=df,
        group_by=group_by,
        n=n,
        x_label=x_label,
        y=y_label,
        separator=separator,
        x_range=x_range,
        bw_method=bw_method
    )

    assert y_label == 'density'
    return line_plot(
        df=density_curve,
        x=x_label,
        y=y_label,
        colour_by=colour_by,
        line_type_by=line_type_by,
        colours=colours,
        line_types=line_types,
        line_opacity=line_opacity,
        title=title,
        x_label=x_label,
        y_label=y_label,
        colour_label=colour_label,
        line_type_label=line_type_label,
        display=display,
        x_range=x_range,
        y_range=y_range,
        line_width=line_width,
        width=width,
        height=height
    )
