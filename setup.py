from setuptools import setup, find_packages
from os import path
from io import open

setup(
    name='sitka',
    version='0.1',
    description='A built environment analysis and modeling library for Python.',
    long_description="""# A library for built environment modeling and simulation
                        directly in Python.""",
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
