#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
  Do some cleaning!

"""
try:
    import os
    from distutils.dir_util import remove_tree
    from shutil import copyfile
except ImportError:


def cleanDir(directory):
    if os.path.exists(directory):
        print("Cleaning directory: " + directory + "\n")
        for f in os.listdir(directory):
            if not os.path.isdir(os.path.join(directory, f)) \
                    and not f.lower().endswith(".pyc") and not f.lower().endswith(".py"):
                os.remove(os.path.join(directory, f))
        for f in os.listdir(directory):
            if not os.path.isdir(f) and f.lower().endswith(".pyc"):
                copyfile(os.path.join(directory, f), os.path.join(directory, f[:-5]))


print("Starting clean.\n")

_Py_file_loc = os.path.dirname(os.path.realpath(__file__))
_sample_dir = os.path.join(_Py_file_loc, "sample")

# Delete the distribution dir if it exists
if os.path.exists(_dist_dir):
    print("Removing dist directory: " + _sample_dir + "\n")
    remove_tree(_dist_dir, verbose=1)

# Clean the config dir
cleanDir(_config_dir)

# Clean the samples dir
cleanDir(_sample_dir)

# Clean .pyc files
print("Cleaning .pyc files")
for root, dirs, files in os.walk(_Py_file_loc):
    for file in files:
        full_path = os.path.join(root, file)
        if full_path.lower().endswith(".pyc"):
            os.remove(full_path)

