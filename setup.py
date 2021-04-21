#!/usr/bin/env python
"""Censys Maltego Setup."""
import os
from setuptools import setup, find_packages

GIT_URL = "https://github.com/censys/censys-maltego"

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = "\n" + f.read()

setup(
    name="censys_maltego",
    version="2.0.0.b1",
    description="This package provides an interface into Censys from Maltego.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Censys Team",
    author_email="support@censys.io",
    license="Apache License, Version 2.0",
    keywords=["censys", "search", "maltego"],
    python_requires=">=3.6.0",
    packages=find_packages("src"),
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
    package_data={
        "": ["*.gif", "*.png", "*.conf", "*.mtz", "*.machine"]  # list of resources
    },
    install_requires=[
        "canari>=3.3.10,<4",
        "censys==2.0.0b2",
    ],
    extras_require={
        "dev": [
            "flake8==3.9.1",
            "flake8-docstrings==1.6.0",
            "flake8-pytest-style==1.4.1",
            "flake8-simplify==0.14.0",
            "flake8-comprehensions==3.4.0",
            "pep8-naming==0.11.1",
            "flake8-black==0.2.1",
            "black==20.8b1",
            "mypy==0.812",
            "twine==3.4.1",
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
