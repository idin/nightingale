import pytest
import pandas as pd
import numpy as np
from nightingale.plots import density_plot
from nightingale.distribution import probability_density_curve

def test_probability_density_curve():
    """Test the probability_density_curve function."""
    # Create a sample DataFrame
    data = {
        'x': np.random.normal(loc=0, scale=1, size=1000),
        'group1': np.random.choice(['A', 'B'], size=1000),
        'group2': np.random.choice(['C', 'D'], size=1000)
    }
    df = pd.DataFrame(data)

    # Test without grouping
    density_curve = probability_density_curve(x='x', df=df, n=100)
    assert 'x' in density_curve.columns
    assert 'density' in density_curve.columns
    assert len(density_curve) == 100

    # Test with grouping
    density_curve_grouped = probability_density_curve(x='x', df=df, n=100, group_by='group1')
    assert 'x' in density_curve_grouped.columns
    assert 'density' in density_curve_grouped.columns
    assert 'group1' in density_curve_grouped.columns
    assert len(density_curve_grouped) > 0  # Ensure some data is returned
    assert len(density_curve_grouped) == 100 * 2 # 2 groups

def test_density_plot():
    """Test the density_plot function."""
    # Create a sample DataFrame
    data = {
        'x': np.random.normal(loc=0, scale=1, size=1000),
        'group1': np.random.choice(['A', 'B'], size=1000),
        'group2': np.random.choice(['C', 'D'], size=1000)
    }
    df = pd.DataFrame(data)

    # Test density plot without grouping
    fig = density_plot(df=df, x='x', color=None)
    assert fig is not None  # Ensure a figure is returned

    # Test density plot with grouping
    fig_grouped = density_plot(df=df, x='x', color='group1')
    assert fig_grouped is not None  # Ensure a figure is returned

    # Check if the figure has the expected data
    # fig_grouped.data[0].x is array of size 100
    assert len(fig_grouped.data[0].x) == 100
    assert isinstance(fig_grouped.data[0].x, np.ndarray)
    # for y
    assert len(fig_grouped.data[0].y) == 100
    assert isinstance(fig_grouped.data[0].y, np.ndarray)

if __name__ == "__main__":
    pytest.main() 
