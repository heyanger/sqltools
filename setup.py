#!/usr/bin/env python

from distutils.core import setup
from glob import glob

from setuptools import find_packages

setup(name='sqltools',
      version='0.0.1',
      description='sql tools for tree building/sequence generation',
      author='He Yang, Er',
      packages=find_packages('sqltools'),
      package_dir={'': 'sqltools'},
     )