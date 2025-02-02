from setuptools import setup, find_packages

setup(
    name='nightingale',
    version='0.1.0',
    author='Idin Karuei',
    author_email='python@idin.net',
    description='A wrapper for Plotly to simplify visualizations and plots.',
    packages=find_packages(),
    license="Conditional Freedom License (CFL-1.0)",
    install_requires=[
        'plotly>=5.0.0',  # Specify the version of Plotly you want to support
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