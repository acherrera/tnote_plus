"""
Defines the setup for the pypi package
"""

from setuptools import setup, find_packages
from io import open
from os import path
import pathlib

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read()

setup(
    name="tnote_plus",
    description="A simple note taking app",
    version="0.0.2",
    packages=find_packages(),  # list of all packages
    install_requires=requirements,
    python_requires=">=3.8",
    entry_points="""
        [console_scripts]
        tnote=src.tnote:main
    """,
    author="Anthony Herrera",
    keyword="notes, note taking, simple",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://github.com/acherrera/tnote_plus",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
    ],
)
