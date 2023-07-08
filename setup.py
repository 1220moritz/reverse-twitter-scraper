from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ReverseTwitterScraper",
    version="0.8",
    author="1220moritz",
    description="A Python package for scraping Twitter data without API. With proxy and account-cookie support",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/1220moritz/reverse-twitter-scraper",
      install_requires=[
          'selenium-wire',
          'selenium',
          "httpx",
          "asyncio"
      ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    project_urls={
        "Documentation": "https://github.com/1220moritz/reverse-twitter-scraper/blob/main/README.md",
        "Github": "https://github.com/1220moritz/reverse-twitter-scraper",
        "PyPi": "https://pypi.org/project/ReverseTwitterScraper/",
        "Contact": "https://discordapp.com/users/713118695165263923",
    },
)
