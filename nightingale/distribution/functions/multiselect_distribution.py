"""Sampling utilities for generating data"""

import numpy as np
import pandas as pd

def multiselect_distribution(category_probs, n, max_selection_probs=None, output_type='dataframe', seed=None):
    """
    Generate samples for categories with True/False values based on probabilities,
    limiting the number of True values per row to a random number x, based on x_probs.
    
    Parameters:
        category_probs (dict): A dictionary where keys are categories (str) and values are probabilities (0 to 1).
        n (int): Number of samples to generate.
        max_selection_probs (dict): A dictionary where keys are possible values (int) and values are probabilities (0 to 1).
                        Sum of probabilities must be 1, and max(max_selection_probs.keys()) <= len(category_probs).
                        The values are the number of selected categories, for example if the value is 2, then at most 2 categories can be True
                        if max_selection_probs is None, then the number of selected categories is not limited
        output_type (str): Output format, either 'dataframe' or 'array'. Defaults to 'dataframe'.
        seed (int, optional): Seed for reproducibility. Defaults to None.
    """
    if output_type not in {'dataframe', 'array', 'dictionary'}:
        raise ValueError("output_type must be 'dataframe' or 'array'")
    
    if seed is not None:
        np.random.seed(seed)
    
    categories = np.array(list(category_probs.keys()))
    probabilities = np.array(list(category_probs.values()))
    
    # Validate inputs
    if not all(0 <= p <= 1 for p in probabilities):
        raise ValueError("All probabilities must be between 0 and 1.")
    
    # Generate raw probabilities for each category
    raw_choices = np.random.rand(n, len(categories)) < probabilities

    if max_selection_probs is None:
        # return the categories chosen
        if output_type == 'dataframe':
            return pd.DataFrame(raw_choices, columns=categories)
        elif output_type == 'array':
            return raw_choices
        elif n == 1:
            return {category: raw_choices[0][i] for i, category in enumerate(categories)}
        else:
            raise ValueError(f"Invalid output type: {output_type}")

    if not np.isclose(sum(max_selection_probs.values()), 1.0):
        raise ValueError("n_category_probs must sum to 1.")
    if max(max_selection_probs.keys()) > len(categories):
        raise ValueError("Max x in n_category_probs cannot exceed the number of categories.")

    # Generate the random x values based on max_selection_probs
    max_selection_values = np.random.choice(
        list(max_selection_probs.keys()), size=n, p=list(max_selection_probs.values())
    )
    
    # Sort indices by random priority to determine which True values to keep
    priority = np.argsort(np.random.rand(n, len(categories)), axis=1)
    sorted_choices = np.take_along_axis(raw_choices, priority, axis=1)
    
    # Create mask to limit True values to x per row
    mask = np.arange(len(categories)) < max_selection_values[:, None]
    limited_choices = np.zeros_like(sorted_choices, dtype=bool)
    limited_choices[mask] = sorted_choices[mask]
    
    # Revert sorted choices back to original order
    unsorted_choices = np.zeros_like(limited_choices, dtype=bool)
    unsorted_choices[np.arange(n)[:, None], priority] = limited_choices
    
    # Output as DataFrame or NumPy array
    if output_type == 'dataframe':
        return pd.DataFrame(unsorted_choices, columns=categories)
    elif output_type == 'array':
        return unsorted_choices
    elif n == 1 and output_type == 'dictionary':
        d = {category: unsorted_choices[0][i] for i, category in enumerate(categories)}
        return {key: bool(value) for key, value in d.items()}
    else:
        raise ValueError(f"Invalid output type: {output_type}")

# Example usage
"""
category_probs = {'A': 0.7, 'B': 0.4, 'C': 0.9, 'D': 0.6}
n = 10
max_selection_probs = {1: 0.2, 2: 0.5, 3: 0.3}  # Probability distribution for x
seed = 42

result_df = limited_multiselect_distribution(category_probs, n, max_selection_probs, output_type='dataframe', seed=seed)
result_array = limited_multiselect_distribution(category_probs, n, max_selection_probs, output_type='array', seed=seed)

print("DataFrame Output:\n", result_df)
print("\nNumPy Array Output:\n", result_array)
"""