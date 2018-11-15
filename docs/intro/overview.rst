===============
Overview
===============

Sitka is intended for conducting analyses directly in Python data analysis
pipelines and workflows.  One primary use is to develop Jupyter notebooks
for common analyses that don't require full building energy models.  This
may be useful for interactive analyses that often occur during early design,
prototyping simulation models, or embedding analyses into web services.

The library is intended to supplement the use cases for established building
energy simulation cases (e.g. code and green building rating system compliance),
rather than to replace those tools.

The project also intends to test concepts not currently found in existing
applications, such as:

- Allow a model to be updated when an attribute is changed.
- Store object data for re-use and connection to visualization and analysis.
- Define the simulation scope by using as much or as little of the library as desired.
- Allow for easily hackable models.  Modify or add modules and classes, as needed.

The highly coupled and large scale of building simulation means that it is
expected that there will be limitations in the model size and simulation
performance.  While the project is beginning completely in Python, it is
expected that C objects or enhanced solvers may be leveraged to improve
performance for some models. 
