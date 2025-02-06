import pytest
from nightingale.plots import density_plot
from nightingale.distribution import normal_distribution
import pandas as pd
import numpy as np

def test_density_plot():
    display = True
    n = 1000
    x1 = normal_distribution(n=n, mean=0, std=1)
    x2 = normal_distribution(n=n, mean=2, std=0.5)
    x3 = normal_distribution(n=n, mean=4, std=0.2)

    df1 = pd.DataFrame({
        'x1': x1,
        'x2': x2,
        'x3': x3
    })

    fig1 = density_plot(x=df1['x1'], bw_method=0.1)
    assert fig1 is not None

    assert 'x1' in df1.columns
    fig2 = density_plot(df=df1, x='x1')
    assert fig2 is not None

    # test providing x as a list of column names:
    fig3 = density_plot(df=df1, x=['x1', 'x2', 'x3'], colour_by='colourful')
    assert fig3 is not None

    df2 = pd.DataFrame({
        'x': np.concatenate([x1, x2, x3]),
        'group': np.concatenate([['x1']*n, ['x2']*n, ['x3']*n])
    })

    if display:
        fig1.show()
        fig2.show()
        fig3.show()
