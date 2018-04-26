# -*- coding: utf-8 -*-

import os
from setuptools import setup

# Function for the readme file
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "pyPolar",
    version = "0.1.0",
    author = "Jack Ogaja",
    author_email = "jack_ogaja@brown.edu",
    description = (" Data processing tool for Polar Lows research "
                   " by Institute at Brown for Environment and Society(IBES), Brown University"),
    license = "MIT",
    keywords = "AIS",
    url = "https://gitlab.com/lynch_lab/pyPolar",
    packages=['pp_core', 'polar_pp'],
    long_description=read('README.rst'),
    classifiers=[
        "Development Status :: 5 - Stable",
        "Topic :: Data Analysis",
        "License :: OSI Approved :: MIT License",
    ],
)


