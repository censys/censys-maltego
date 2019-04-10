import setuptools
from setuptools import find_packages

setuptools.setup(
    name="censys_maltego",
    version="1.1.0",
    author="Art Sturdevant",
    author_email="support@censys.io",
    description="This package provides an interface into Censys from Maltego.",
    install_requires=['censys', 'maltego-trx'],
    packages=find_packages(),
    py_modules=['censys_maltego'],
    python_requires='>=3'
)
