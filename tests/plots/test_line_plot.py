from nightingale.plots import line_plot
import pandas as pd
import numpy as np

def test_line_plot():
    display = False
    x = list(range(100))
    y = [np.sin(i/3) for i in x]
    colour = ['colour_a'] * 30 + ['colour_b'] * 70
    line_type = ['line_type_1'] * 70 + ['line_type_2'] * 30
    df = pd.DataFrame({'x': x, 'y': y, 'colour': colour, 'line_type': line_type})
    line_plot(df=df, x='x', y='y', line_opacity=0.5, line_width=2, colour_by='colour', line_type_by='line_type', x_label='This is X', title='This is Title', colour_label='This is Colour', line_type_label='This is Line Type')

    line_plot(df=df, x='x', y='y')

    # test display
    fig = line_plot(df=df, x='x', y='y', display=True)
    assert fig is None

    # test colour
    fig = line_plot(df=df, x='x', y='y', colour_by='x')
    assert fig is not None

    # test line type
    line_plot(df=df, x='x', y='y', line_type_by='x')
    
    # test line opacity
    line_plot(df=df, x='x', y='y', line_opacity=0.5)

    # test line width
    line_plot(df=df, x='x', y='y', line_width=2)
    
    # test all
    line_plot(
        df=df, x='x', y='y', line_opacity=0.5, line_width=2, colour_by='colour', line_type_by='line_type', 
        x_label='This is X', y_label='This is Y', title='This is Title', colour_label='This is Colour', line_type_label='This is Line Type',
        width=800, height=1000,
        display=display
    )

    # test dictating colour red
    red = '#FF0000'
    fig = line_plot(df=df, x='x', y='y', colours=red)
    assert fig is not None
    if display:
        fig.show()


    # test dictating line type solid
    dot = 'dot'
    fig = line_plot(df=df, x='x', y='y', line_types=dot)
    assert fig is not None
    if display:
        fig.show()


    # test mapping colours
    colours = {'colour_a': red, 'colour_b': 'blue'}
    fig = line_plot(df=df, x='x', y='y', colour_by='colour', colours=colours)
    assert fig is not None
    if display:
        fig.show()


    # test listing colours
    colours = [red, 'green']
    fig = line_plot(df=df, x='x', y='y', colour_by='colour', colours=colours)
    assert fig is not None
    if display:
        fig.show()


    # test single colour
    colours = 'purple'
    fig = line_plot(df=df, x='x', y='y', colour_by='colour', colours=colours)
    assert fig is not None
    if display:
        fig.show()
    

    # test listing line types
    line_types = [dot, 'dash']
    fig = line_plot(df=df, x='x', y='y', line_types=line_types)
    assert fig is not None
    if display:
        fig.show()
    