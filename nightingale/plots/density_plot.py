from ..distribution import probability_density_curve
import pandas as pd
from typing import Optional, Union
import plotly.express as px
import numpy as np

def density_plot(
    x: Union[pd.Series, np.ndarray, list, str],
    df: Optional[pd.DataFrame] = None,
    color: Optional[Union[str, list]] = None,
    title: Optional[str] = None,
    x_label: Optional[str] = None,

    y_label: Optional[str] = 'density',
    n: int = 100,
    x_range: Optional[Union[list, tuple]] = None,
    separator: Optional[str] = '  ',
    bw_method: Optional[float] = 0.1
):
    """
    Create a density plot, optionally decomposed by group so their sum
    matches the single global KDE. Uses the above probability_density_curve.
    """
    if isinstance(x, str):
        x_label_display = x_label or x
    else:
        x_label_display = x_label or 'x'


    # Generate the density curve (either global or partial by group)
    density_curve = probability_density_curve(
        x=x,
        df=df,
        group_by=color,
        n=n,
        y=y_label,
        separator=separator,
        x_range=x_range,
        bw_method=bw_method
    )

    # If color was a list, ensure the correct label
    if isinstance(color, list):
        if len(color) == 1:
            color = color[0]
        else:
            color = 'group'

    fig = px.line(
        density_curve,
        x=x,
        y=y_label,
        color=color,
        title=title,
        labels={'x': x_label_display, 'y': y_label}
    )
    return fig
