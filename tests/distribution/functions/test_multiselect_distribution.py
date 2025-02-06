import pytest
from nightingale.distribution.functions import multiselect_distribution
import pandas as pd
import numpy as np

def test_multiselect_distribution():
    category_probs = {'A': 0.9, 'B': 0.8}
    max_selection_probs = {1: 0.9, 2: 0.1}

    # output types
    assert isinstance(multiselect_distribution(category_probs=category_probs, max_selection_probs=max_selection_probs, n=1000, output_type='dataframe'), pd.DataFrame)
    assert isinstance(multiselect_distribution(category_probs=category_probs, max_selection_probs=max_selection_probs, n=1000, output_type='array'), np.ndarray)


    # output types even if n is 1
    assert isinstance(multiselect_distribution(category_probs=category_probs, max_selection_probs=max_selection_probs, n=1000, output_type='dataframe'), pd.DataFrame)
    assert isinstance(multiselect_distribution(category_probs=category_probs, max_selection_probs=max_selection_probs, n=1000, output_type='array'), np.ndarray)


    # output cannot be series or value even if n is 1
    with pytest.raises(ValueError):
        multiselect_distribution(category_probs=category_probs, max_selection_probs=max_selection_probs, n=1000, output_type='series')
    with pytest.raises(ValueError):
        multiselect_distribution(category_probs=category_probs, max_selection_probs=max_selection_probs, n=1000, output_type='value')
    with pytest.raises(ValueError):
        multiselect_distribution(category_probs=category_probs, max_selection_probs=max_selection_probs, n=1, output_type='series')
    with pytest.raises(ValueError):
        multiselect_distribution(category_probs=category_probs, max_selection_probs=max_selection_probs, n=1, output_type='value')

    # output should be a dictionary if n is 1 and output_type is not dataframe or array and keys should be the categories and values should be boolean

    assert isinstance(multiselect_distribution(category_probs=category_probs, max_selection_probs=max_selection_probs, n=1, output_type='dictionary'), dict)
    assert all(key in category_probs for key in multiselect_distribution(category_probs=category_probs, max_selection_probs=max_selection_probs, n=1, output_type='dictionary').keys())
    sample = multiselect_distribution(category_probs=category_probs, max_selection_probs=max_selection_probs, n=1, output_type='dictionary')
    for value in sample.values():
        if not isinstance(value, bool):
            print(f'value is not a bool: {value}, type: {type(value)}')
    assert all(isinstance(value, bool) for value in sample.values())

    # test seed
    seed1_dist = multiselect_distribution(category_probs=category_probs, max_selection_probs=max_selection_probs, n=1000, seed=1)
    seed2_dist = multiselect_distribution(category_probs=category_probs, max_selection_probs=max_selection_probs, n=1000, seed=2)
    assert not seed1_dist.equals(seed2_dist)

    seed1_dist = multiselect_distribution(category_probs=category_probs, max_selection_probs=max_selection_probs, n=1000, seed=1)
    seed1_dist2 = multiselect_distribution(category_probs=category_probs, max_selection_probs=max_selection_probs, n=1000, seed=1)
    assert seed1_dist.equals(seed1_dist2)

    seedless_dist1 = multiselect_distribution(category_probs=category_probs, max_selection_probs=max_selection_probs, n=1000)
    seedless_dist2 = multiselect_distribution(category_probs=category_probs, max_selection_probs=max_selection_probs, n=1000)
    assert not seedless_dist1.equals(seedless_dist2)

    # if output type is dataframe, columns should be the categories and values should be boolean

    assert set(multiselect_distribution(category_probs=category_probs, max_selection_probs=max_selection_probs, n=1000, output_type='dataframe').columns.tolist()) == set(category_probs.keys())
    assert set(multiselect_distribution(category_probs=category_probs, max_selection_probs=max_selection_probs, n=1, output_type='dataframe').columns.tolist()) == set(category_probs.keys())

    # if output type is array, values should be boolean
    sample = multiselect_distribution(category_probs=category_probs, max_selection_probs=max_selection_probs, n=1000, output_type='array')
    # check if all columns are boolean
    assert all(isinstance(value, np.bool_) for value in sample.flatten())

    # selections should be less than selection probabilities
    distribution = multiselect_distribution(category_probs=category_probs, max_selection_probs=max_selection_probs, n=1000, output_type='dataframe')
    # number of both selections should be less than 0.1 and number of one selection should be less than 0.9
    # number of selections is number of True values in the row
    num_of_selections = distribution.sum(axis=1)

    num_of_one_selection = (num_of_selections == 1).sum()
    num_of_both_selections = (num_of_selections == 2).sum()
    assert num_of_one_selection / 1000 < 0.9
    assert num_of_both_selections / 1000 < 0.1

    # if output type is dictionary, keys should be the categories and values should be boolean
    assert isinstance(multiselect_distribution(category_probs=category_probs, max_selection_probs=max_selection_probs, n=1, output_type='dictionary'), dict)
    assert all(key in category_probs for key in multiselect_distribution(category_probs=category_probs, max_selection_probs=max_selection_probs, n=1, output_type='dictionary').keys())
    assert all(isinstance(value, bool) for value in multiselect_distribution(category_probs=category_probs, max_selection_probs=max_selection_probs, n=1, output_type='dictionary').values())
