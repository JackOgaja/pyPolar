#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
   Copyright (c) 2017 Jack Ogaja
   All Rights Reserved

   HOS Analytic:
    Set up the package for analysis of Higher Order Schemes.

   Licensce: MIT License
"""

try:
    import os,glob,string,sys
    from numpy.distutils.core import setup, Extension
    from numpy.distutils import fcompiler
    from distutils.dep_util import newer
    setuptools_imported = False
except ImportError:
    setuptools_imported = False

def read(*names, **kwargs):
    with io.open(
                 os.path.join(os.path.dirname(__file__), *names),
                 encoding=kwargs.get("encoding", "utf8")
                 ) as ioR:
        return ioR.read()

def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                                             version_file, re.M)
    if version_match:
                     return version_match.group(1)
                     raise RuntimeError("Unable to find version string.")
                                                      

def get_version():
    basedir = os.path.dirname(__file__)
    try:
        with open(os.path.join(basedir, 'cs_analytic/version.py')) as vp:
            locals = {}
            exec(vp.read(), locals)
            return locals['VERSION']
    except FileNotFoundError:
        raise RuntimeError('No version info found.')

if setuptools_imported:
       add_features = dict(
                      )
else:
       add_features = dict(
       )

setup(
    name='ha',
    version=find_version("package", "__init__.py")
    #++version=get_version(),
    url='https://github.com/Jaecq/cs_analytic/',
    license='MIT License',
    author='Jack Ogaja',
    author_email='jack.ogaja@gmail.com',
    description='Utitlities to analyse Higher Order Schemes  '
    long_description=__doc__,
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=[
        'phynx >= 2.7.0',
    ],
    python_requires='>=2.7',
    entry_points={
        'console_scripts': [
            'hos = hos.qchos:analysis',

        ],
    },
    classifiers=[
        # From http://pypi.python.org/pypi?%3Aaction=list_classifiers
        # 'Development Status :: 1 - Planning',
        # 'Development Status :: 2 - Pre-Alpha',
         'Development Status :: 3 - Alpha',
        # 'Development Status :: 4 - Beta',
        #'Development Status :: 5 - Production/Stable',
        # 'Development Status :: 6 - Mature',
        # 'Development Status :: 7 - Inactive',
        'Intended Audience :: Scientists and Engineers',
        'Intended Audience :: Model Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Science and Engineering',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Operating System :: macOS',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',

    ],
    **add_features
  )

def setupDevel():
    os.system('mkdir -p hos/hos_devel')
    hosDevelFiles = ['__init__.py', '__version__.py', 
                      'hos_functions.py', 'hos_graphics.py']
                      for file in hosDevelFiles:
                           os.system('cp hos/hos-analytic/%s hos/hos_devel/%s' % (file,file))

                      setup(
                            name         = "CS Analytic",
                            version      = open('Version').read()[:-1],
                            description  = "Utilities for Higher Order Conservative Schemes",
                            author       = "Jack Ogaja",
                            author_email = "jack.ogaja@gmail.com",
                            url          = "http://github.com/Jaecq",
                            packages     = ['Hos_devel'],
                            package_dir  = {'hos-analytic':'hos/hos_devel'},
                            )

if Devel:
    setupDevel()
else:
    setup()


