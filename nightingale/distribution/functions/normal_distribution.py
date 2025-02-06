import numpy as np
import pandas as pd
from scipy.stats import truncnorm

def normal_distribution(mean, std, n, name='value', output_type='series', seed=None, min=None, max=None):
    """
    Generate samples from a normal distribution
    The result is pandas Series or numpy array
    If max and min are not None, the samples are truncated to the range [min, max]
    """
    if max is None and min is None:
        if seed is not None:
            np.random.seed(seed)
        samples = np.random.normal(mean, std, size=n)
    else:
        # Ensure min is less than max
        if min is not None and max is not None and min > max:
            raise ValueError("min should be less than max")
        
        # Calculate the truncation bounds
        if min is None:
            min = -np.inf
        if max is None:
            max = np.inf

        a = (min - mean) / std  # Lower bound for truncation
        b = (max - mean) / std  # Upper bound for truncation
        if seed is not None:
            np.random.seed(seed)
        samples = truncnorm.rvs(a, b, loc=mean, scale=std, size=n)

        # print the values that are less than min and raise an error if there are any
        if sum(samples < min) > 0:
            print(samples[samples < min])
            raise ValueError(f"There are {sum(samples < min)} values that are less than min")
        
        # print the values that are greater than max and raise an error if there are any
        if sum(samples > max) > 0:
            print(samples[samples > max])
            raise ValueError(f"There are {sum(samples > max)} values that are greater than max")

    if n == 1 and output_type == 'value':
        return samples[0]

    elif output_type == 'series':
        return pd.Series(samples, name=name)
    
    elif output_type == 'array':
        return samples

    else:
        raise ValueError(f"Invalid output type: {output_type}")
