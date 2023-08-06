#!/usr/bin/env python

"""The setup script."""

from setuptools import find_packages, setup

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("CHANGELOG.rst") as history_file:
    history = history_file.read()

requirements = []

test_requirements = ["pytest"]

setup(
    author="HBN3tw0rk",
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Lesser General Public License v2 (LGPLv2)",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    description="Distributed Cache for Humans",
    install_requires=requirements,
    license="GNU Lesser General Public License v2.1",
    long_description=readme + "\n\n" + history,
    include_package_data=True,
    keywords="dcache",
    name="dcache",
    packages=find_packages(include=["dcache", "dcache.*"]),
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/HBN3tw0rk/dcache",
    version="0.0.2",
    zip_safe=False,
)
