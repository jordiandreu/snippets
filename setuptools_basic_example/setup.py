# coding=utf-8
# setuptools documentation: developers guide
# https://setuptools.readthedocs.io/en/latest/setuptools.html#developer-s-guide

from setuptools import setup, find_packages
setup(
    name = "setuptools_basic_example_pkg",
    version = "0.1",
    packages = find_packages(),
)