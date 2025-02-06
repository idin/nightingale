import pytest
import pandas as pd
import numpy as np
from nightingale.plots.plot_helpers.infer_plot_arguments import infer_plot_arguments
LIST_OF_3_NUMBERS = [1, 2, 3]
ANOTHER_LIST_OF_3_NUMBERS = [4, 5, 6]
SERIES_OF_3_NUMBERS = pd.Series(LIST_OF_3_NUMBERS)
ARRAY_OF_3_NUMBERS = np.array(LIST_OF_3_NUMBERS)

LIST_OF_4_NUMBERS = [1, 2, 3, 4]
SERIES_OF_4_NUMBERS = pd.Series(LIST_OF_4_NUMBERS)
ARRAY_OF_4_NUMBERS = np.array(LIST_OF_4_NUMBERS)

LIST_OF_DIFFERNT_SIZE_LISTS = [LIST_OF_3_NUMBERS, LIST_OF_4_NUMBERS]
LIST_OF_DIFFERNT_SIZE_SERIES = [SERIES_OF_3_NUMBERS, SERIES_OF_4_NUMBERS]
LIST_OF_DIFFERNT_SIZE_ARRAYS = [ARRAY_OF_3_NUMBERS, ARRAY_OF_4_NUMBERS]

DICT_OF_DIFFERNT_SIZE_LISTS = {'A': LIST_OF_3_NUMBERS, 'B': LIST_OF_4_NUMBERS}

LIST_OF_SAME_SIZE_LISTS = [LIST_OF_3_NUMBERS, ANOTHER_LIST_OF_3_NUMBERS]
LIST_OF_SAME_SIZE_SERIES = [SERIES_OF_3_NUMBERS, SERIES_OF_3_NUMBERS]
LIST_OF_SAME_SIZE_ARRAYS = [ARRAY_OF_3_NUMBERS, ARRAY_OF_3_NUMBERS]

def test_one_collection():
    arg = infer_plot_arguments(x=SERIES_OF_3_NUMBERS)

    assert isinstance(arg['df'], pd.DataFrame)
    assert arg['x'] == 'x'
    assert arg['y'] is None
    assert arg['colour_by'] is None
    assert len(arg) == 4

    arg = infer_plot_arguments(x=ARRAY_OF_3_NUMBERS)
    assert isinstance(arg['df'], pd.DataFrame)
    assert arg['x'] == 'x'
    assert arg['y'] is None
    assert arg['colour_by'] is None
    assert len(arg) == 4

    arg = infer_plot_arguments(x=LIST_OF_3_NUMBERS)
    assert isinstance(arg['df'], pd.DataFrame)
    assert 'x' in arg['df'].columns
    assert 'y' not in arg['df'].columns
    assert arg['x'] == 'x'
    assert arg['y'] is None
    assert arg['colour_by'] is None
    assert len(arg) == 4

def test_two_collections():

    # two different sizes should raise an error
    with pytest.raises(ValueError):
        infer_plot_arguments(x=LIST_OF_3_NUMBERS, y=LIST_OF_4_NUMBERS)

    # two same sizes should work
    arg = infer_plot_arguments(x=LIST_OF_3_NUMBERS, y=LIST_OF_3_NUMBERS)
    assert isinstance(arg['df'], pd.DataFrame)
    assert 'x' in arg['df'].columns
    assert 'y' in arg['df'].columns
    assert 'group' not in arg['df'].columns
    assert arg['x'] == 'x'
    assert arg['y'] == 'y'
    assert arg['colour_by'] is None
    assert len(arg) == 4

def test_one_list_of_collections():
    arg = infer_plot_arguments(x=LIST_OF_DIFFERNT_SIZE_LISTS)
    assert isinstance(arg['df'], pd.DataFrame)
    assert arg['df'].shape == (7, 2)
    assert 'x' in arg['df'].columns
    assert 'group' in arg['df'].columns
    assert 'y' not in arg['df'].columns
    assert arg['x'] == 'x'
    assert arg['y'] is None
    assert arg['colour_by'] == 'group'
    assert len(arg) == 4
    # one group should have 3 values, the other should have 4
    assert len(arg['df'][arg['df']['group'] == 'group_0'] == 3)
    assert len(arg['df'][arg['df']['group'] == 'group_1'] == 4)

    # if colour_by is provided, it should be the same as the group column
    arg = infer_plot_arguments(x=LIST_OF_DIFFERNT_SIZE_LISTS, colour_by='MYGROUP')
    assert arg['colour_by'] == 'MYGROUP'
    # size of groups should be 4 and 3
    df = arg['df']
    assert len(df[df['MYGROUP'] == 'MYGROUP_0']) == 3
    assert len(df[df['MYGROUP'] == 'MYGROUP_1']) == 4

def test_one_dict_of_collections():
    arg = infer_plot_arguments(x=DICT_OF_DIFFERNT_SIZE_LISTS)
    assert isinstance(arg['df'], pd.DataFrame)
    assert arg['df'].shape == (7, 2)
    assert 'x' in arg['df'].columns
    assert 'group' in arg['df'].columns
    assert 'y' not in arg['df'].columns
    # group names should be the keys of the dictionary
    df = arg['df']
    assert len(df[df['group'] == 'A']) == 3
    assert len(df[df['group'] == 'B']) == 4

    # if colour_by is provided, it should be the same as the group column
    arg = infer_plot_arguments(x=DICT_OF_DIFFERNT_SIZE_LISTS, colour_by='COLOUR_BY')
    assert arg['colour_by'] == 'COLOUR_BY'
    assert len(arg) == 4
    df = arg['df']
    assert len(df[df['COLOUR_BY'] == 'A']) == 3
    assert len(df[df['COLOUR_BY'] == 'B']) == 4

def test_one_list_of_collections_and_a_collection():
    assert ANOTHER_LIST_OF_3_NUMBERS == [4, 5, 6]
    # sizes should be the same
    with pytest.raises(ValueError):
        infer_plot_arguments(x=LIST_OF_DIFFERNT_SIZE_ARRAYS, y=LIST_OF_3_NUMBERS)

    # sizes should be the same
    with pytest.raises(ValueError):
        infer_plot_arguments(x=LIST_OF_3_NUMBERS, y=LIST_OF_DIFFERNT_SIZE_ARRAYS)

    # sizes should be the same
    with pytest.raises(ValueError):
        infer_plot_arguments(x=LIST_OF_SAME_SIZE_ARRAYS, y=LIST_OF_4_NUMBERS)

    # sizes should be the same
    with pytest.raises(ValueError):
        infer_plot_arguments(x=LIST_OF_4_NUMBERS, y=LIST_OF_SAME_SIZE_SERIES)

    # if sizes are the same, it should work
    arg = infer_plot_arguments(x=[LIST_OF_3_NUMBERS, ANOTHER_LIST_OF_3_NUMBERS], y=LIST_OF_3_NUMBERS)
    assert isinstance(arg['df'], pd.DataFrame)
    assert arg['df'].shape == (6, 3)
    assert 'x' in arg['df'].columns
    assert 'y' in arg['df'].columns
    assert 'group' in arg['df'].columns
    assert arg['x'] == 'x'
    assert arg['y'] == 'y'
    assert arg['colour_by'] == 'group'
    assert len(arg) == 4
    # number of both groups should be 3
    df = arg['df']
    assert len(df[df['group'] == 'group_0']) == 3
    assert len(df[df['group'] == 'group_1']) == 3
    # values of y should be correct
    assert set(df['y'].values) == set(LIST_OF_3_NUMBERS)
    # values of x should be correct
    group_0 = df[df['group'] == 'group_0']
    assert set(group_0['x'].values) == set(LIST_OF_3_NUMBERS)
    group_1 = df[df['group'] == 'group_1']
    assert set(group_1['x'].values) == set(ANOTHER_LIST_OF_3_NUMBERS)

    del arg
    del df

    # swap x and y
    assert ANOTHER_LIST_OF_3_NUMBERS == [4, 5, 6]

    y_list_of_list_arg = infer_plot_arguments(x=LIST_OF_3_NUMBERS, y=[LIST_OF_3_NUMBERS, ANOTHER_LIST_OF_3_NUMBERS])
    assert isinstance(y_list_of_list_arg['df'], pd.DataFrame)
    assert y_list_of_list_arg['df'].shape == (6, 3) 

    assert 'x' in y_list_of_list_arg['df'].columns
    assert 'y' in y_list_of_list_arg['df'].columns
    assert 'group' in y_list_of_list_arg['df'].columns
    assert y_list_of_list_arg['x'] == 'x'
    assert y_list_of_list_arg['y'] == 'y'
    # values of y should be correct
    assert set(y_list_of_list_arg['df']['y'].values) == set(LIST_OF_3_NUMBERS + ANOTHER_LIST_OF_3_NUMBERS)

    # values of group_1 should be correct
    df = y_list_of_list_arg['df']
    group_1 = df[df['group'] == 'group_1']
    assert set(group_1['y'].values) == set(ANOTHER_LIST_OF_3_NUMBERS)
    assert y_list_of_list_arg['colour_by'] == 'group'

    del df

    # if colour_by is provided, it should be the same as the group column
    arg = infer_plot_arguments(x=LIST_OF_3_NUMBERS, y=[LIST_OF_3_NUMBERS, ANOTHER_LIST_OF_3_NUMBERS], colour_by='COLOUR_BY')
    assert arg['colour_by'] == 'COLOUR_BY'
    assert len(arg) == 4
    df = arg['df']
    assert len(df[df['COLOUR_BY'] == 'COLOUR_BY_0']) == 3
    assert len(df[df['COLOUR_BY'] == 'COLOUR_BY_1']) == 3
    assert set(df['y'].values) == set(LIST_OF_3_NUMBERS + ANOTHER_LIST_OF_3_NUMBERS)
