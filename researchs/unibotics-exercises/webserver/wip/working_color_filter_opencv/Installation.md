
////////////////////////////////////////////////////////////////////////////////
                I N S T A L L A T I O N     R E C I P E
////////////////////////////////////////////////////////////////////////////////

The infrastructure of this exercise is composed of:

    - Jupyter
    - OpenCV
    - Python 2

If you want to solve the ColorFilter through your local camera (i.e. webcam),
you just need to install the following:

1. Some distributions, such as Fedora, don’t come with Python 2 pre-installed. 
You can install the python2 package with your distribution package manager:
`$ sudo dnf install python2`

2. Install the Jupyter Project (http://jupyter.org/install)
`$ python -m pip install --upgrade pip`
`$ python -m pip install jupyter`

3. Install OpenCV (Computer Vision Library):
`$ sudo apt-get install python-opencv`

Open Python IDLE (or IPython) and type following codes in Python terminal.
'''
        import cv2 as cv
        print(cv.__version__)
'''
If the results are printed out without any errors, congratulations !!! 
You have installed OpenCV-Python successfully.

Additionally, this Jupyter Notebook uses some extensions to improve the user 
experience and facilitate coding and debugging tasks. You can install those extensions
following the next steps (https://github.com/ipython-contrib/jupyter_contrib_nbextensions):

4. All of the nbextensions in the extensions repo are provided as parts of a python package, 
which is installable in the usual manner, using pip or the setup.py script. 
To install the current version from PyPi, simply type:

`$ pip install jupyter_contrib_nbextensions`

Alternatively, you can install directly from the current master branch of the repository ->

`$ pip install https://github.com/ipython-contrib/jupyter_contrib_nbextensions/tarball/master`

Then, install required javascript and css files:

`$ jupyter contrib nbextension install --user`

Finally, enable the required extensions:
`$ sudo jupyter nbextension enable init_cell/main`
`$ sudo jupyter nbextension enable hide_input/main`

NOW YOU ARE READY TO START CODING. YOU WILL FIND SOME HELP IN THE NOTEBOOK
(color_filter.ipynb). GOOD LUCK!




