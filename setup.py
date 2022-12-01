#!/usr/bin/env python
"""Censys Maltego Setup."""
import os
from setuptools import setup, find_packages

GIT_URL = "https://github.com/censys/censys-maltego"

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = "\n" + f.read()

setup(
    name="censys-maltego",
    version="2.0.0",
    description="This package provides an interface into Censys from Maltego.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Censys Team",
    author_email="support@censys.io",
    license="Apache License, Version 2.0",
    keywords=["censys", "search", "maltego"],
    python_requires=">=3.6.0",
    packages=find_packages("src", exclude=["tests"]),
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
    package_data={
        "": ["*.gif", "*.png", "*.conf", "*.mtz", "*.machine"]  # list of resources
    },
    install_requires=[
        "canari>=3.3.10,<4",
        "censys==2.0.9",
    ],
    extras_require={
        "dev": [
            "flake8==4.0.1",
            "flake8-docstrings==1.6.0",
            "flake8-pytest-style==1.6.0",
            "flake8-simplify==0.15.2",
            "flake8-comprehensions==3.8.0",
            "pep8-naming==0.12.1",
            "flake8-black==0.3.4",
            "black==22.10.0",
            "pytest==7.0.1",
            "pytest-cov==3.0.0",
            "responses==0.18.0",
            "mypy==0.981",
            "twine==4.0.2",
            "parameterized==0.8.1",
        ]
    },
    classifiers=[
        "Topic :: Internet",
        "Topic :: Security",
        "Topic :: Internet :: WWW/HTTP :: Indexing/Search",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Framework :: Flake8",
        "Natural Language :: English",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    project_urls={
        "Censys Homepage": "https://censys.io/",
        "Changelog": GIT_URL + "/releases",
        "Tracker": GIT_URL + "/issues",
        "Source": GIT_URL,
    },
)
