import numpy as np
import pandas as pd
from typing import Union, Any

def categorical_distribution(category_probs, n, name='value', output_type='series', seed=None):
    """
    Generate samples for categories with probabilities.

    Args:
        category_probs (dict): A dictionary where keys are categories and values are their probabilities.
        n (int): Number of samples to generate.
        name (str): Name for the resulting Series (if output_type is 'series').
        output_type (str): Format of the output ('series', 'array', or 'value').
        seed (int, optional): Seed for random number generation.

    Returns:
        Union[pd.Series, np.ndarray, Any]: Generated samples in the specified format.
    """
    categories = list(category_probs.keys())

    probabilities = list(category_probs.values())
    if seed is not None:
        np.random.seed(seed)
    samples = np.random.choice(categories, size=n, p=probabilities)

    if n == 1 and output_type == 'value':
        value = samples[0]
        if isinstance(value, (np.int64, np.int32)):
            return int(value)
        else:
            return value
    elif output_type == 'series':
        return pd.Series(samples, name=name)

    elif output_type == 'array':
        return samples       

    else:
        raise ValueError(f"Invalid output type: {output_type}")
