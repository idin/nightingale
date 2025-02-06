import pytest
import numpy as np
from nightingale.distribution.functions.normal_distribution import normal_distribution
import pandas as pd

def test_normal_distribution():
    assert normal_distribution(0, 1, 1000) is not None

    # test output type
    assert isinstance(normal_distribution(mean=0, std=1, n=1000, output_type='series'), pd.Series)
    assert isinstance(normal_distribution(mean=0, std=1, n=1000, output_type='array'), np.ndarray)
    # output should be series or array even if n is 1
    assert isinstance(normal_distribution(mean=0, std=1, n=1, output_type='series'), pd.Series)
    assert isinstance(normal_distribution(mean=0, std=1, n=1, output_type='array'), np.ndarray)

    # output should be a value if n is 1 and output_type is not series or array
    assert isinstance(normal_distribution(mean=0, std=1, n=1, output_type='value'), float)

    # test seed
    seedless_dist = normal_distribution(mean=0, std=1, n=1000)
    seedless_dist2 = normal_distribution(mean=0, std=1, n=1000)
    assert isinstance(seedless_dist, pd.Series)
    assert isinstance(seedless_dist2, pd.Series)
    # count number of values that are the same
    same_values = sum(seedless_dist.values == seedless_dist2.values)
    different_values = sum(seedless_dist.values != seedless_dist2.values)
    assert different_values == 1000

    seed_dist = normal_distribution(mean=0, std=1, n=1000, seed=1)
    seed_dist2 = normal_distribution(mean=0, std=1, n=1000, seed=1)
    assert sum(seed_dist == seed_dist2) == 1000
    assert sum(seed_dist != seed_dist2) == 0

    # test min and max
    # assert normal_distribution(mean=0, std=1, n=1000, min=0, max=1) is not None
    # if min is greater than max, raise an error
    with pytest.raises(ValueError):
        normal_distribution(mean=0, std=1, n=1000, min=1, max=0)

    # if min is provided values should be greater than or equal to min
    # count number of values that are greater than and less than min
    dist = normal_distribution(mean=0.5, std=1, n=1000, min=0)
    greater_than_min = sum(dist >= 0)
    less_than_min = sum(dist < 0)
    if less_than_min > 0:
        # print the values that are less than min
        print(dist[dist < 0])
    
    assert greater_than_min + less_than_min == 1000
    assert less_than_min == 0
    assert greater_than_min == 1000

    # if max is provided values should be less than or equal to max
    dist = normal_distribution(mean=0, std=1, n=1000, max=1)
    greater_than_max = sum(dist > 1)
    less_than_max = sum(dist <= 1)
    assert greater_than_max == 0
    assert less_than_max == 1000

    # if min and max are provided, values should be between min and max
    dist = normal_distribution(mean=0, std=1, n=1000, min=0, max=1)
    greater_than_min = sum(dist >= 0)
    less_than_max = sum(dist <= 1)
    assert greater_than_min == 1000
    assert less_than_max == 1000

    # size of the output should be n
    assert len(normal_distribution(mean=0, std=1, n=1000, min=0, max=1)) == 1000
    assert len(normal_distribution(mean=0, std=1, n=1, min=0, max=1)) == 1

    # if series is provided name should be the name of the series
    assert normal_distribution(mean=0, std=1, n=1000, name='test', output_type='series').name == 'test'
    assert normal_distribution(mean=0, std=1, n=1000, name='other_name', output_type='series').name == 'other_name'
    assert normal_distribution(mean=0, std=1, n=1, output_type='series').name == 'value'
