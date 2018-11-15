from setuptools import setup, find_packages
from os import path
from io import open

setup(
    name='sitka',
    version='0.1.2',
    description='A built environment analysis and modeling library for Python.',
    long_description="""
    Sitka is a built environment analysis and modeling library for Python.

    This library is intended to make modeling and simulation for the built environment more hackable and easier to use for:

    * Portable design tools
    * Scalable web apps and services
    * Quick design and analysis studies
    * Interactive simulations and analyses
    * Testing new models

    The library is currently being written entirely in Python using [Pandas](https://pandas.pydata.org) as a core dependency in order to allow easier integration with data analysis in [Jupyter](https://jupyter.org).

    A focus of this project is to create tools to make building models more hackable.  The library can be used to create a simple model just a few inputs or a larger whole building model can be created by connecting multiple objects.

    """,
    long_description_content_type='text/markdown',
    url='https://github.com/mcneillj/sitka',
    author='James McNeill',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='simulation setuptools development',
    packages=find_packages(include=['sitka', 'sitka.*']),
    include_package_data=True,
    install_requires=[
        "numpy>=1.14.3",
        "pandas>=0.23.0",
        "pytest>=3.5.1",
    ],
)
