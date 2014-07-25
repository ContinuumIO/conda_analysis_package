#!/usr/bin/env python
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.version_info[:2] < (2, 7):
    sys.exit("conda is only meant for Python 2.7, with experimental support "
             "for python 3.  current version: %d.%d" % sys.version_info[:2])

setup(
    name = "conda-analysis-package",
    version="0.2.0",
    author = "Continuum Analytics, Inc.",
    author_email = "ilan@continuum.io",
    url = "https://github.com/ContinuumIO/conda-analysispackage",
    license = "BSD",
    classifiers = [
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
    ],
    description = "tools for building conda packages",
    packages = ['conda_analysis_package'],
    scripts = [
        'bin/conda-analysispackage',
        ],
    install_requires = ['conda'],
)
