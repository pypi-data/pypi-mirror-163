#!/usr/bin/env python
import sys
from setuptools import setup, find_namespace_packages

if sys.version_info < (3, 7):
    print('Error: Soda SQL requires at least Python 3.7')
    print('Error: Please upgrade your Python version to 3.7 or later')
    sys.exit(1)

package_name = "soda-sql-trino"
package_version = '2.2.2'
description = "Soda SQL Trino"

requires = [
    f'soda-sql-core=={package_version}',
    'trino>=0.305.0'
]

setup(
    name=package_name,
    version=package_version,
    install_requires=requires,
    packages=find_namespace_packages(include=["sodasql*"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ]
)
