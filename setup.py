#!/usr/bin/env python3
# -*- coding=utf-8 -*-
r"""

"""
import sys; sys.path.append('./src')  # noqa
import setuptools
from inifini import __author__, __version__, __description__, __license__


install_requires = []

development_requires = ["better-exceptions"]
all_requires = [development_requires]
extras_require = {
    'development': development_requires,
    'all': all_requires,
}

setuptools.setup(
    name="inifini",
    version=__version__,
    description=__description__,
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author=__author__,
    license=__license__,
    url="https://github.com/PlayerG9/inifini",
    project_urls={
        "Author Github": "https://github.com/PlayerG9",
        "Homepage": "https://github.com/PlayerG9/inifini",
        # "Documentation": "https://PlayerG9.github.io/inifini/",
        "Bug Tracker": "https://github.com/PlayerG9/inifini/issues",
    },
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Environment :: Web Environment",
        "Topic :: Internet",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: HTTP Servers",
        # "Topic :: Internet :: WWW/HTTP :: WSGI",
        # "Topic :: Internet :: WWW/HTTP :: WSGI :: Server",
    ],
    python_requires=">=3.7",
    install_requires=install_requires,
    extras_require=extras_require,
    # test_suite="tests",
    entry_points={
        "console_scripts": [
            "inifini = inifini.__main__:main"
        ]
    },
)
