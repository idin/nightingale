from typing import Optional, Union, Dict, Any
import pandas as pd
import numpy as np

def is_label_different_from_column(label, column, label_name=None):
    if not isinstance(label, str):
        if label_name is not None:
            raise TypeError(f"{label_name} must be a string, got {type(label)}")
        raise TypeError(f"label must be a string, got {type(label)}")
    
    if label is not None and isinstance(column, str):
        return label != column
    return False

def get_plot_kwargs(
        x: Optional[str] = None,
        y: Optional[str] = None,
        df: Optional[pd.DataFrame] = None,
        title: Optional[str] = None,
        x_label: Optional[str] = None,
        y_label: Optional[str] = None,
        colour_by: Optional[str] = None,
        colour_label: Optional[str] = None,
        line_type_by: Optional[str] = None,
        line_type_label: Optional[str] = None,
        size_by: Optional[str] = None,
        size_label: Optional[str] = None,
        size_max: Optional[float] = None,
        colours: Optional[Union[str, list, Dict[str, str]]] = None,
        line_types: Optional[Union[str, list, Dict[str, str]]] = None,
        line_opacity: Optional[float] = 1,
        line_width: Optional[float] = 2,
        x_range: Optional[Union[list, tuple]] = None,
        y_range: Optional[Union[list, tuple]] = None,
        width: Optional[int] = None,
        height: Optional[int] = None
) -> Dict[str, Dict[str, Any]]:
    """
    Process common plot parameters and return arguments for figure updates.
    """
    
    if isinstance(x, str):
        x_label = x_label or x
    else:
        x_label = x_label or 'x'

    if isinstance(y, str):
        y_label = y_label or y
    else:
        y_label = y_label or 'y'

    if isinstance(colour_by, str):
        colour_label = colour_label or colour_by
    else:
        colour_label = colour_label or 'colour'

    if isinstance(line_type_by, str):
        line_type_label = line_type_label or line_type_by
    else:
        line_type_label = line_type_label or 'line_type'

    if isinstance(size_by, str):
        size_label = size_label or size_by

    else:
        size_label = size_label or 'size'

    labels = {}
    if is_label_different_from_column(label=x_label, column=x, label_name='x_label'):
        labels['x'] = x_label
    if is_label_different_from_column(label=y_label, column=y, label_name='y_label'):
        labels['y'] = y_label
    if is_label_different_from_column(label=colour_label, column=colour_by, label_name='colour_label'):
        labels['colour'] = colour_label
    if is_label_different_from_column(label=line_type_label, column=line_type_by, label_name='line_type_label'):
        labels['line_type'] = line_type_label
    if is_label_different_from_column(label=size_label, column=size_by, label_name='size_label'):
        labels['size'] = size_label

    # make sure the columns of df are unique
    column_names = df.columns.tolist()
    if len(column_names) != len(set(column_names)):
        raise ValueError("The columns of df must be unique.")

    # if colours is provided, it should override the colours used in the plot
    plot_kwargs = {
        'data_frame': df,
        'x': x,
        'y': y,
        'color': colour_by,
        'line_dash': line_type_by,
        'title': title,
        'size': size_by,
        'size_max': size_max,
        # 'size_min': size_min
    }

    update_traces_kwargs = {}
    update_layout_kwargs = {}

    if colours is not None:
        if isinstance(colours, list):
            plot_kwargs['color_discrete_sequence'] = colours
        elif isinstance(colours, dict):
            plot_kwargs['color_discrete_map'] = colours

        elif isinstance(colours, str):
            update_traces_kwargs['line'] = {'color': colours}

    if line_types is not None:
        if isinstance(line_types, list):
            plot_kwargs['line_dash_sequence'] = line_types
        elif isinstance(line_types, dict):
            plot_kwargs['line_dash_map'] = line_types

        elif isinstance(line_types, str):
            update_traces_kwargs['line'] = {'dash': line_types}

    if line_opacity is not None:
        update_traces_kwargs['opacity'] = line_opacity

    if line_width is not None:
        update_traces_kwargs['line_width'] = line_width

    if x_range is not None:
        update_layout_kwargs['xaxis_range'] = x_range

    if y_range is not None:
        update_layout_kwargs['yaxis_range'] = y_range

    if width is not None:
        update_layout_kwargs['width'] = width

    if height is not None:
        update_layout_kwargs['height'] = height

    result = {
        'plot_kwargs': plot_kwargs,
        'update_traces_kwargs': update_traces_kwargs, 
        'update_layout_kwargs': update_layout_kwargs
    }

    # remove None values
    result = {
        kwarg_name: {key: value for key, value in kwarg.items() if value is not None}
        for kwarg_name, kwarg in result.items()
    }

    result['all_kwargs'] = dict(
        x=plot_kwargs.get('x', None),
        y=plot_kwargs.get('y', None),
        df=plot_kwargs.get('data_frame', None),
        colour_by=plot_kwargs.get('color', None),
        line_type_by=plot_kwargs.get('line_dash', None),
        size_by=plot_kwargs.get('size', None),

        title=plot_kwargs.get('title', None),
        x_label=labels.get('x', None),
        y_label=labels.get('y', None),
        colour_label=labels.get('colour', None),
        line_type_label=labels.get('line_type', None),
        size_label=labels.get('size', None),

        size_max=plot_kwargs.get('size_max', None),
        colours=plot_kwargs.get('color_discrete_sequence', plot_kwargs.get('color_discrete_map', None)),
        line_types=plot_kwargs.get('line_dash_sequence', plot_kwargs.get('line_dash_map', None)),
        line_opacity=plot_kwargs.get('opacity', None),
        line_width=plot_kwargs.get('line_width', None),

        x_range=update_layout_kwargs.get('xaxis_range', None),
        y_range=update_layout_kwargs.get('yaxis_range', None),
        width=update_layout_kwargs.get('width', None),
        height=update_layout_kwargs.get('height', None)
    )
    assert isinstance(result['all_kwargs']['x'], str)

    return result
