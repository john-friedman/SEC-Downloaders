from setuptools import setup, find_packages

from pathlib import Path
long_description = Path("../readme.md").read_text()

setup(
    name="sec_downloaders",
    author="John Friedman",
    version="0.003",
    description = "A package to download SEC filings",
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[
        'requests',
        'pandas',
    ],
    url="https://github.com/john-friedman/SEC-Downloaders",
    package_data={
        "data": ["*.csv"],
    },
    include_package_data=True,
)