from setuptools import setup, find_packages
from pathlib import Path

VERSION = '0.0.1'
DESCRIPTION = "A request based package for scraping twitter data. No API Key required. Support for proxies and private twitter accounts."
long_description = (Path(__file__).parent / "readme.md").read_text()

# Setting up
setup(
    name="ReverseTwitterScraper",
    version=VERSION,
    author="1220.moritz",
    #author_email="<not@available.com>",
    url = 'https://github.com/1220moritz/reverse-twitter-scraper',
    description=DESCRIPTION,
    long_description=long_description,
    license_files = ('LICENSE.txt',),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=["time", "seleniumwire", "selenium", "requests-python"],
    keywords=['twitter', 'noApi', 'scraping', 'reverse'],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
