#!/usr/bin/env python

from distutils.core import setup

setup(name='python-unfuddle',
      version='1.0',
      description='Python API for Unfuddle',
      author='Ryan Nowakowski',
      author_email='tubaman@fattuba.com',
      py_modules=['unfuddle'],
      install_requires=["requests>=2.2.1"],
     )
