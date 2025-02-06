import pandas as pd
import numpy as np
from nightingale.distribution.functions.categorical_distribution import categorical_distribution

def test_categorical_distribution():
    category_probs = {'A': 0.7, 'B': 0.2, 'C': 0.1}
    assert categorical_distribution(category_probs=category_probs, n=1000) is not None

    # test output type
    assert isinstance(categorical_distribution(category_probs=category_probs, n=1000, output_type='series'), pd.Series)
    assert isinstance(categorical_distribution(category_probs=category_probs, n=1000, output_type='array'), np.ndarray)

    # output should be series or array even if n is 1
    assert isinstance(categorical_distribution(category_probs=category_probs, n=1, output_type='series'), pd.Series)
    assert isinstance(categorical_distribution(category_probs=category_probs, n=1, output_type='array'), np.ndarray)

    # output should be a value if n is 1 and output_type is not series or array
    assert isinstance(categorical_distribution(category_probs=category_probs, n=1, output_type='value'), str)

    # output should be a number if categories are a dictionary of numbers
    dist = categorical_distribution(category_probs={1: 0.7, 2: 0.2, 3: 0.1}, n=1, output_type='value')
    if not isinstance(dist, int):
        raise ValueError(f"dist is not an int: {dist} but a {type(dist)}")
    assert isinstance(categorical_distribution(category_probs={1: 0.7, 2: 0.2, 3: 0.1}, n=1, output_type='value'), int)

    # output should be one of the categories
    assert categorical_distribution(category_probs=category_probs, n=1, output_type='value') in category_probs

    # test seed
    seed1_dist = categorical_distribution(category_probs=category_probs, n=1000, seed=1)
    seed2_dist = categorical_distribution(category_probs=category_probs, n=1000, seed=2)
    n_equal = sum(seed1_dist == seed2_dist)
    assert n_equal < 1000

    # test seedless
    seedless_dist = categorical_distribution(category_probs=category_probs, n=1000)
    seedless_dist2 = categorical_distribution(category_probs=category_probs, n=1000)
    n_equal = sum(seedless_dist == seedless_dist2)
    assert n_equal < 1000

    # with seed
    seed_dist = categorical_distribution(category_probs=category_probs, n=1000, seed=1)
    seed_dist2 = categorical_distribution(category_probs=category_probs, n=1000, seed=1)
    n_equal = sum(seed_dist == seed_dist2)
    assert n_equal == 1000

    # test name
    assert categorical_distribution(category_probs=category_probs, n=1000, name='test') is not None    

    # if output is series, name should be the name of the series
    assert categorical_distribution(category_probs=category_probs, n=1000, name='test', output_type='series').name == 'test'
    assert categorical_distribution(category_probs=category_probs, n=1, name='test', output_type='series').name == 'test'
    assert categorical_distribution(category_probs=category_probs, n=1000, output_type='series').name == 'value'
