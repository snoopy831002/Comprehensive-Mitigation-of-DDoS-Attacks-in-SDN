#!/usr/bin/env python
'''Setuptools params'''

from setuptools import setup, find_packages

setup(
    name='switch',
    version='0.0.0',
    description='',
    author='',
    author_email='',
    packages=find_packages(exclude='test'),
    package_dir = {'': 'pox_module'}
)

