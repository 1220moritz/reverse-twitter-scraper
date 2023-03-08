from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ReverseTwitterScraper",
    version="0.0.3",
    author="1220moritz",
    description="A Python package for scraping Twitter data without API. With proxy and account-cookie support",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/1220moritz/reverse-twitter-scraper",
      install_requires=[
          'selenium-wire',
          'selenium',
          "requests",
      ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)