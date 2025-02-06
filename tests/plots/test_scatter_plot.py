import pytest
import pandas as pd
import numpy as np
from nightingale.plots.scatter_plot import scatter_plot
import pandas as pd
import numpy as np

def test_scatter_plot():
    display = True
    x = list(range(100))
    y = [np.sin(i/3) for i in x]
    colour = ['colour_a'] * 30 + ['colour_b'] * 70
    size = [10] * 30 + [20] * 70

    df = pd.DataFrame({'x': x, 'y': y, 'colour': colour, 'size': size})
    scatter_plot(df=df, x='x', y='y', size_by='size', colour_by='colour', x_label='This is X', title='This is Title', colour_label='This is Colour', size_label='This is Size', display=display)


    # test display
    fig = scatter_plot(df=df, x='x', y='y', display=False)
    assert fig is not None

    fig = scatter_plot(df=df, x='x', y='y', display=True)
    assert fig is None


    # test colour
    fig = scatter_plot(df=df, x='x', y='y', colour_by='x')
    assert fig is not None


    # test size
    fig = scatter_plot(df=df, x='x', y='y', size_by='x')
    assert fig is not None

    # test all
    scatter_plot(
        df=df, x='x', y='y', size_by='size', colour_by='colour', 
        x_label='This is X', y_label='This is Y', title='This is Title', colour_label='This is Colour', size_label='This is Size',
        width=800, height=1000,
        display=display
    )

    # test dictating colour red
    red = '#FF0000'
    fig = scatter_plot(df=df, x='x', y='y', colours=red)
    assert fig is not None
    if display:
        fig.show()

    # test mapping colours
    colours = {'colour_a': red, 'colour_b': 'blue'}
    fig = scatter_plot(df=df, x='x', y='y', colour_by='colour', colours=colours)
    assert fig is not None
    if display:
        fig.show()

    # test listing colours
    colours = [red, 'green']
    fig = scatter_plot(df=df, x='x', y='y', colour_by='colour', colours=colours)
    assert fig is not None
    if display:
        fig.show()

    # test single colour
    colours = 'purple'
    fig = scatter_plot(df=df, x='x', y='y', colour_by='colour', colours=colours)
    assert fig is not None
    if display:
        fig.show()
