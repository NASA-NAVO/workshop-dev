# workshop-dev
Python workshop development and scratch area.
# Setup
Within a suitable Python environment, Python code and notebooks at the top level can easily import and run the utility code.  This is one way to set up such an environment:
```
conda create --name workshop-dev python=3.6 astropy matplotlib requests notebook
conda activate workshop-dev
conda install -c astropy astroquery
```
