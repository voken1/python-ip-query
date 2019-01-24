#!/usr/bin/env python
# encoding: utf-8

from setuptools import (setup, find_packages)

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name="ip-query",
    version="3.1.9",
    packages=find_packages(),

    # metadata for upload to PyPI
    author="Vision Network",
    author_email="michael@vision.network",
    description="Python IP Query.",
    keywords='Python, IP, IP address, IP GEO',

    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/VisionNetworkProject/python-ip-query",

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

    install_requires=[
        'requests[socks]',
        'geoip2',
    ],
)
