import pytest
import numpy as np
import pandas as pd

def uniform_distribution(min, max, n, name='value', output_type='series', seed=None):
    """
    Generate samples from a uniform distribution
    """
    if min > max:
        raise ValueError("min should be less than max")

    if seed is not None:
        np.random.seed(seed)

    samples = np.random.uniform(min, max, size=n)

    if n == 1 and output_type not in {'series', 'array'}:
        return samples[0]
    
    elif output_type == 'series':
        return pd.Series(samples, name=name)
    
    elif output_type == 'array':
        return samples
    
    else:
        raise ValueError(f"Invalid output type: {output_type}")
