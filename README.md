# [Sitka](http://www.sitka.io/) &middot; [![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/mcneillj/sitka/blob/master/LICENSE) [![codecov](https://codecov.io/gh/mcneillj/sitka/branch/master/graph/badge.svg)](https://codecov.io/gh/mcneillj/sitka) [![Build Status](https://travis-ci.org/mcneillj/sitka.svg?branch=master)](https://travis-ci.org/mcneillj/sitka)

Sitka is a built environment analysis and modeling library for Python.

This library is intended to make modeling and simulation for the built environment more hackable and easier to use for:

* Portable design tools
* Scalable web apps and services
* Quick design and analysis studies
* Interactive simulations and analyses
* Testing new models

The library is currently being written entirely in Python using [Pandas](https://pandas.pydata.org) as a core dependency in order to allow easier integration with data analysis in [Jupyter](https://jupyter.org).

A focus of this project is to create tools to make building models more hackable.  The library can be used to create a simple model just a few inputs or a larger whole building model can be created by connecting multiple objects.

## Installation

You can install Sitka on your local machine, virtualenv, or server.  It is completely written in Python, so it is easily portable to any machine with Python installed.  The `sitka` package is available on [pypi](https://pypi.org/project/sitka/).  The latest version can be installed using pip.

```sh
# using PyPI
pip install sitka
```

## Dependencies
- [NumPy](https://www.numpy.org): 1.9.0 or higher
- [Pandas](https://pandas.pydata.org): 0.23.0 or higher

## Features
* **Weather** - Import a weather file in EPW format and convert
* **Solar:** Calculate solar angles for a site and determine solar radiation on surfaces.
* **Envelope and Constructions (FUTURE):** Wall and window construction models.
* **Thermal Zone (FUTURE):** Model thermal zones using the Heat Balance Method.
* **HVAC Systems (FUTURE):** Model air-side and water-side HVAC systems.

## Documentation

You can find the documentation [on the website](http://www.sitka.io).  

## Examples

Example files are provided in the [sitka-examples repo](https://www.github.com/mcneillj/sitka-examples).

## Contributing

Contributors are welcome.  You can start by submitting an [issue](https://www.github.com/mcneillj/sitka/issues).

### License

React is [MIT licensed](./LICENSE).
