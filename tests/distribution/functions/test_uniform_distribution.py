import pytest
from nightingale.distribution.functions.uniform_distribution import uniform_distribution
import pandas as pd
import numpy as np

def test_uniform_distribution():
    # uniform distribution gets min and max as arguments
    assert uniform_distribution(0, 1, 1000) is not None

    # test output type
    assert isinstance(uniform_distribution(min=0, max=1, n=1000, output_type='series'), pd.Series)
    assert isinstance(uniform_distribution(min=0, max=1, n=1000, output_type='array'), np.ndarray)

    # output should be series or array even if n is 1
    assert isinstance(uniform_distribution(min=0, max=1, n=1, output_type='series'), pd.Series)
    assert isinstance(uniform_distribution(min=0, max=1, n=1, output_type='array'), np.ndarray)

    # output should be a value if n is 1 and output_type is not series or array
    assert isinstance(uniform_distribution(min=0, max=1, n=1, output_type='value'), float)

    # test seed
    dist1 = uniform_distribution(min=0, max=1, n=1000, seed=1)
    dist2 = uniform_distribution(min=0, max=1, n=1000, seed=2)
    dist3 = uniform_distribution(min=0, max=1, n=1000, seed=1)
    dist4 = uniform_distribution(min=0, max=1, n=1000)

    dist5 = uniform_distribution(min=0, max=1, n=1000)

    # dist 1 and dist 2 should be different, they are series, so comparing the values, but not all values are different some can be the same
    assert sum(dist1 != dist2) > 0

    # dist 1 and dist 3 should be the same, they are series, so comparing the values
    assert sum(dist1 == dist3) == 1000

    # dist 1 and dist 4 should be different, they are series, so comparing the values
    assert sum(dist1 == dist4) < 1000

    # dist 4 and 5 should be different, they are series, so comparing the values
    assert sum(dist4 == dist5) < 1000

    # test min and max
    assert uniform_distribution(min=0, max=1, n=1000) is not None
    # if min is greater than max, raise an error
    with pytest.raises(ValueError):
        uniform_distribution(min=1, max=0, n=1000)

    # values should be between min and max
    assert np.all(uniform_distribution(min=0, max=1, n=1000) >= 0)
    assert np.all(uniform_distribution(min=0, max=1, n=1000) <= 1)

    # size of the output should be n
    assert len(uniform_distribution(min=0, max=1, n=1000)) == 1000
    assert len(uniform_distribution(min=0, max=1, n=1)) == 1

    # if series is provided name should be the name of the series
    assert uniform_distribution(min=0, max=1, n=1000, name='test', output_type='series').name == 'test'
    assert uniform_distribution(min=0, max=1, n=1000, name='other_name', output_type='series').name == 'other_name'
    assert uniform_distribution(min=0, max=1, n=1, output_type='series').name == 'value'
