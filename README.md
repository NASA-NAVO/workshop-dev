# workshop-dev
Python workshop development and scratch area.
# Setup
Within a suitable Python environment, Python code and notebooks at the top level can easily import and run the utility code.  This is one way to set up such an environment:
```
conda env create -f environment.yml
conda activate navo-workshop
```

# Updating development versions
The environment may include some development versions. To update to the latest:
```
conda env update --file environment.yml --prune
```

# Starting Jupyterlab
From the directory containing the notebooks:
```
jupyter lab
```

# Demo in Binder
This badge opens Jupyterlab session on Binder which can be used to run the workshop notebooks.
Note that the session will disapper after being left unattended for several minutes.

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/NASA-NAVO/workshop-dev/master?urlpath=lab)
