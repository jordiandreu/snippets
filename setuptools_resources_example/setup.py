# coding=utf-8
# setuptools documentation: developers guide
# https://setuptools.readthedocs.io/en/latest/setuptools.html#developer-s-guide

from setuptools import setup, find_packages
setup(
    name = "setuptools_resource_example_pkg",
    version = "0.1",
    packages = find_packages('src'),
    package_dir = {'':'src'},
    include_package_data = True,
    package_data = {'mypkg': ['resources/*.png', 'resources/*.svg'],}
)