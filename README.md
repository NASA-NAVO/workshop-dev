# workshop-dev
Python workshop development and scratch area.
# Setup
Within a suitable Python environment, Python code and notebooks at the top level can easily import and run the utility code.  This is one way to set up such an environment:
```
conda create --name workshop-dev -c conda-forge python=3.6 astropy matplotlib requests notebook astroquery scipy aplpy 
conda activate workshop-dev

Currently using development version of pyvo, so:

git clone https://github.com/astropy/pyvo.git
cd pyvo
python setup.py develop

(which allows you to 'git pull' as pyvo develops).
```
