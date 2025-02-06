from nightingale.plots.plot_helpers import melt
from nightingale.plots.plot_helpers import get_plot_kwargs
from nightingale.plots.plot_helpers import infer_plot_arguments
import pandas as pd

def test_melt():
    df = pd.DataFrame({'x': [1, 2, 3], 'y': [4, 5, 6], 'z': [7, 8, 9], 'other': [10, 11, 12], 'another': [13, 14, 15]})
    assert df.shape == (3, 5)

    melted_df = melt(df=df, columns=['x', 'y', 'z'], group_column='group')
    assert melted_df.shape == (9, 4)
    assert 'group' in melted_df.columns
    assert 'value' in melted_df.columns
    assert 'x' not in melted_df.columns
    assert 'y' not in melted_df.columns
    assert 'z' not in melted_df.columns

    # column group should only have 3 unique values
    assert melted_df['group'].nunique() == 3

    # those should be x, y, z
    assert set(melted_df['value'].values) == set(range(1, 10))
    assert set(melted_df['group'].values) == set(['x', 'y', 'z'])


    x = list(melted_df[melted_df['group'] == 'x']['value'].values)
    y = list(melted_df[melted_df['group'] == 'y']['value'].values)
    z = list(melted_df[melted_df['group'] == 'z']['value'].values)

    assert x == [1, 2, 3]
    assert y == [4, 5, 6]
    assert z == [7, 8, 9]

    # if group and value are provided, they should be used as the group and value columns
    melted_df = melt(df=df, columns=['x', 'y', 'z'], group_column='my group', value_column='my value')
    assert melted_df.shape == (9, 4)
    assert 'my group' in melted_df.columns
    assert 'my value' in melted_df.columns
    assert 'x' not in melted_df.columns
    assert 'y' not in melted_df.columns
    assert 'z' not in melted_df.columns
    assert 'group' not in melted_df.columns
    assert 'value' not in melted_df.columns

def test_melting_colour():
    df = pd.DataFrame({'x1': [1, 2, 3, 4], 'x2': [4, 5, 6, 7], 'x3': [7, 8, 9, 10], 'other': [10, 11, 12, 13], 'another': [13, 14, 15, 16]})

    # give multiple columns as x
    inferred_kwargs = infer_plot_arguments(
        df=df,
        x=['x1', 'x2', 'x3'],
        y='other',
        colour_by='group_colour'
    )
    assert 'y' not in df.columns

    new_df = inferred_kwargs['df']
    x = inferred_kwargs['x']
    y = inferred_kwargs['y']
    colour_by = inferred_kwargs['colour_by']
    del inferred_kwargs

    assert 'other' in new_df.columns
    assert 'y' not in new_df.columns
    assert 'colour' not in new_df.columns
    assert 'group_colour' in new_df.columns
    assert 'x' in new_df.columns
    assert 'x1' not in new_df.columns
    assert 'x2' not in new_df.columns
    assert 'x3' not in new_df.columns
    assert set(new_df['group_colour'].values) == set(['x1', 'x2', 'x3'])
    
    print(new_df.columns)
    assert new_df.shape == (12, 4)
    assert set(new_df.columns) == {'x', 'other', 'group_colour', 'another'}
    assert set(new_df['x'].values) == {1, 2, 3, 4, 5, 6, 7, 8, 9, 10}

