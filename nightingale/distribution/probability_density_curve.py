import numpy as np
import pandas as pd
import math
from typing import Optional, Union
from scipy.stats import gaussian_kde
import plotly.express as px

def probability_density_curve(
    x: Union[pd.Series, np.ndarray, list, str],
    df: Optional[pd.DataFrame] = None,
    n: int = 100,
    group_by: Optional[Union[str, list]] = None,
    y: Optional[str] = 'density',
    separator: Optional[str] = '  ',
    x_range: Optional[Union[list, tuple]] = None,
    bw_method: Optional[float] = 0.1
):
    """
    Create a density curve, optionally decomposed by group in a way that sums
    to the global KDE. Uses a vectorized approach to avoid slow Python loops.
    """

    # --- Helper function for univariate Gaussian ---
    def gauss(u):
        return (1.0 / math.sqrt(2.0 * math.pi)) * np.exp(-0.5 * u**2)

    # --- Handle "no grouping" case ---
    if group_by is None:
        # Single KDE over all data
        if isinstance(x, str):
            x_label = x
            x_vals = df[x].to_numpy()
        else:
            x_label = 'x'
            x_vals = np.array(x)

        # Fit global KDE with desired bandwidth
        kde = gaussian_kde(x_vals)
        if bw_method is not None:
            kde.set_bandwidth(bw_method=bw_method)

        # Evaluate over requested range
        if x_range is None:
            x_min, x_max = x_vals.min(), x_vals.max()
        else:
            x_min, x_max = x_range

        xs = np.linspace(x_min, x_max, n)
        density = kde(xs)

        return pd.DataFrame({x_label: xs, y: density})

    # --- Decompose one global KDE by group ---
    else:
        if not (isinstance(group_by, (str, list)) and df is not None and isinstance(x, str)):
            raise ValueError("group_by must be a column name, df must be provided, and x must be str.")

        # Extract data for global KDE
        x_vals = df[x].to_numpy()
        kde = gaussian_kde(x_vals)
        if bw_method is not None:
            kde.set_bandwidth(bw_method=bw_method)

        # Extract the bandwidth (for 1D, cov is 1×1)
        bandwidth = float(np.sqrt(kde.covariance))

        # Setup x-values to evaluate
        if x_range is None:
            x_min, x_max = x_vals.min(), x_vals.max()
        else:
            x_min, x_max = x_range
        xs = np.linspace(x_min, x_max, n)

        # Number of data points
        N = len(x_vals)

        # --- Build big matrix (n × N) of kernel contributions ---
        # For each x in xs, compute gauss((x - each data point)/bw).
        # shape => xs[:,None] -> (n,1), x_vals[None,:] -> (1,N) => result (n,N).
        Xdiff = (xs[:, None] - x_vals[None, :]) / bandwidth
        Kmat = gauss(Xdiff)  # shape (n, N)
        # Scale by 1/(N*bw) so summing columns gives partial density for a subset
        Kmat /= (N * bandwidth)

        # Now sum columns by group:
        # group_by can be multiple columns or single, handle uniformly
        grouping_cols = [group_by] if isinstance(group_by, str) else group_by
        grouped = df.groupby(grouping_cols)

        df_list = []

        for group_vals, group_df in grouped:
            # Convert group_vals to a tuple if it's not already
            if not isinstance(group_vals, tuple):
                group_vals = (group_vals,)

            # Indices of rows in df that belong to this group
            # shape => (group_size,)
            idx = group_df.index.to_numpy()

            # Sum across the relevant columns of Kmat
            # partial_density has shape (n,)
            partial_density = Kmat[:, idx].sum(axis=1)

            # Build a DataFrame with x and partial density
            part_df = pd.DataFrame({x: xs, y: partial_density})

            # Attach the group labels
            if len(grouping_cols) == 1:
                part_df[grouping_cols[0]] = group_vals[0]
            else:
                # Combine multiple group columns into e.g. 'group'
                group_str = separator.join(
                    f"{col}={val}" for col, val in zip(grouping_cols, group_vals)
                )
                part_df['group'] = group_str

            df_list.append(part_df)

        return pd.concat(df_list, ignore_index=True)
