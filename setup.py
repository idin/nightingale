from setuptools import setup, find_packages

setup(
    name='nightingale',
    version='2025.2.6.1',
    author='Idin K',
    author_email='python@idin.net',
    description='A Python package for creating interactive visualizations and plots using Plotly. Nightingale simplifies the process of generating various types of plots, including scatter plots, line plots, and density plots, with customizable options for colours, sizes, and more.',
    url='https://github.com/idin/nightingale',
    packages=find_packages(),
    license="Conditional Freedom License (CFL-1.0)",
    install_requires=[
        'plotly>=5.0.0',  
        'pandas>=2.0.0',
        'numpy>=1.20.0',
    ],


    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: Other/Proprietary License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
) 