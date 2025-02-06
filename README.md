# Nightingale

Nightingale is a Python package designed for visualization and plotting. It aims to provide users with powerful tools to create insightful and informative visual representations of data.

## Features

- Easy-to-use interface for creating various types of plots.
- Customizable visualizations to suit your needs.
- Supports multiple data formats.

## Installation

To install Nightingale, you can use pip:

```bash
pip install nightingale
```

## Usage

Here's a simple example of how to use Nightingale:

### Plotting Principles
The best way to use `line_plot`, `scatter_plot`, `density_plot`, or any other plotting function in Nightingale is to pass in a pandas DataFrame and specify the columns you want to plot.
However, you can also pass in a single pandas Series or numpy array, or a list of numbers as x and y values.
You can also pass a list or dictionary of lists of numbers or a list or dictionary of pandas Series or numpy arrays as one of x or y values. 
If you pass a list or dictionary of a collection (list, Series, array) as x or y, or you pass a list of column names, the function will understand that you want to compare them, and uses colours to differentiate between them.

### Line Plot


```python
import nightingale as ng

# Example code to create a line plot from a pandas DataFrame

df = pd.DataFrame({
    'x': [1, 2, 3, 4, 5],
    'y': [1, 2, 3, 4, 5]
})

ng.line_plot(df, x='x', y='y') # returns a Figure object
ng.line_plot(df, x='x', y='y', display=True) # displays the plot and returns None

# Example code to create a line plot and using colours to differentiate between lines

df = pd.DataFrame({
    'x': [1, 2, 3, 4, 5, 1, 2, 3, 4, 5],
    'y': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    'group': ['a', 'a', 'a', 'a', 'a', 'b', 'b', 'b', 'b', 'b']
})

ng.line_plot(df, x='x', y='y', colour_by='group')

# Example code to create a line plot and using line types to differentiate between lines

df = pd.DataFrame({
    'x': [1, 2, 3, 4, 5, 1, 2, 3, 4, 5],
    'y': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    'group': ['a', 'a', 'a', 'a', 'a', 'b', 'b', 'b', 'b', 'b']
})

ng.line_plot(df, x='x', y='y', line_type_by='group')

# Example code to create a line plot and using line types and colours to differentiate between lines

df = pd.DataFrame({
    'x': [1, 2, 3, 4, 5] * 4,
    'y': range(20),
    'group1': ['a'] * 10 + ['b'] * 10,
    'group2': ['c'] * 5 + ['d'] * 5 + ['c'] * 5 + ['d'] * 5
})

ng.line_plot(df, x='x', y='y', colour_by='group1', line_type_by='group2')

# Example code to create a line plot from a single pandas Series or numpy array

x = pd.Series([1, 2, 3, 4, 5])
y = pd.Series([1, 2, 3, 4, 5])

ng.line_plot(x, y)

# Example code to create a line plot from a list of column names

df = pd.DataFrame({
    'x1': [1, 2, 3, 4, 5],
    'x2': [6, 7, 8, 9, 10],
    'y1': [1, 2, 3, 4, 5],
    'y2': [6, 7, 8, 9, 10]
})

ng.line_plot(df, x=['x1', 'x2'], y='y1') # This will use different colours for the two lines defined by x1 and x2
ng.line_plot(df, x='x1', y=['y1', 'y2']) # This will use different colours for the two lines defined by y1 and y2

# Example code to create a line plot from a list of lists or arrays or Series

x_list = [1, 2, 3, 4, 5]
y_list = [1, 2, 3, 4, 5]

ng.line_plot(x_list, y_list)


x_array = np.array([1, 2, 3, 4, 5])
y_array = np.array([1, 2, 3, 4, 5])

ng.line_plot(x_array, y_array)
ng.line_plot(x_list, y_array) # It's ok to pass different types as long as they are the same length

x_series = pd.Series([1, 2, 3, 4, 5])
y_series = pd.Series([1, 2, 3, 4, 5])

ng.line_plot(x_series, y_series)

# Example of code to create a line plot from a list or dictionary of collections

x1 = [1, 2, 3, 4, 5]
x2 = [6, 7, 8, 9, 10]
y1 = [1, 2, 3, 4, 5]
y2 = [6, 7, 8, 9, 10]

ng.line_plot(x=[x1, x2], y=y1) # This will use different colours for the two lines defined by x1 and x2
ng.line_plot(x=x1, y=[y1, y2]) # This will use different colours for the two lines defined by y1 and y2


# Example code to create a plot from a list or dictionary of collections

x1 = [1, 2, 3, 4, 5]
x2 = [6, 7, 8, 9, 10]
y1 = [1, 2, 3, 4, 5]
y2 = [6, 7, 8, 9, 10]

ng.line_plot(x={'group1': x1, 'group2': x2}, y=y1) # This will use different colours for the two lines defined by x1 and x2 and uses the keys of the dictionary to label the lines in the legend
ng.line_plot(x=x1, y={'group1': y1, 'group2': y2}) # This will use different colours for the two lines defined by y1 and y2 and uses the keys of the dictionary to label the lines in the legend

```

### Scatter Plot

The `scatter_plot` is almost identical to the `line_plot` in usage. However, it does not have `line_types` but has two additional arguments:
- `size_by`: a column name or a list of numbers or a pandas Series or a numpy array or a list of pandas Series or a list of numpy arrays to use for the size of the points.
- `size_max`: the maximum size of the points.

```python

# Example code to create a scatter plot from a pandas DataFrame


df = pd.DataFrame({
    'x': [1, 2, 3, 4, 5],
    'y': [1, 2, 3, 4, 5]
})

ng.scatter_plot(df, x='x', y='y')


# Example code to create a scatter plot and using size to differentiate between points

df = pd.DataFrame({
    'x': [1, 2, 3, 4, 5],
    'y': [1, 2, 3, 4, 5],
    'z': [1, 2, 3, 4, 5]
})

ng.scatter_plot(df, x='x', y='y', size_by='z', size_max=10)

# Example code to create a scatter plot from a dictionary of collections

x1 = [1, 2, 3, 4, 5]
x2 = [6, 7, 8, 9, 10]
y1 = [1, 2, 3, 4, 5]
y2 = [6, 7, 8, 9, 10]

ng.scatter_plot(x={'group1': x1, 'group2': x2}, y=y1) # This will use different colours for the two lines defined by x1 and x2 and uses the keys of the dictionary to label the lines in the legend
ng.scatter_plot(x=x1, y={'group1': y1, 'group2': y2}) # This will use different colours for the two lines defined by y1 and y2 and uses the keys of the dictionary to label the lines in the legend

```



## License


This project is licensed under the **Conditional Freedom License (CFL-1.0)**. 

### Usage Restrictions

This software **may NOT** be used, modified, or distributed by:

- Entities opposing women's reproductive rights.
- Entities opposing LGBTQ+ rights.
- Organizations advocating for tariffs and sanctions against Canada.
- Political parties, think tanks, and advocacy groups that support authoritarianism, white supremacy, or fascism.
- Individuals and businesses affiliated with Donald Trump or his political organizations.
- Companies and organizations that deny or obstruct climate science or promote climate disinformation.
- Media outlets that propagate hate speech, conspiracy theories, or extreme political propaganda.
- Companies profiting from war, mass surveillance, and militarization.

For more details, please refer to the LICENSE file.
