"""Setup script for pyuegc."""

import os
from setuptools import setup, find_packages

URL = "https://github.com/mlodewijck/pyuegc"


def get_version():
    version_file = os.path.join("pyuegc", "_version.py")
    namespace = {}
    with open(version_file) as f:
        exec(compile(f.read(), version_file, "exec"), namespace)
    return namespace["__version__"]

with open("README.md", encoding="utf-8") as f:
    README = f.read()

setup(
    name="pyuegc",
    version=get_version(),
    description=(
        "An implementation of the Unicode algorithm for breaking code point "
        "sequences into extended grapheme clusters as specified in UAX #29."
    ),
    long_description=README,
    long_description_content_type="text/markdown",
    author="Marc Lodewijck",
    author_email="mlodewijck@gmail.com",
    license="MIT",
    url=URL,
    project_urls={
        "Bug Reports": "{}/issues".format(URL),
        "Source": "{}/".format(URL),
    },
    keywords=[
        "Unicode",
        "Unicode grapheme clusters",
        "extended grapheme clusters",
        "EGC",
        "grapheme clusters",
        "graphemes",
        "segmentation",
    ],
    # Trove classifiers
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development",
        "Topic :: Software Development :: Internationalization",
        "Topic :: Text Processing",
        "Topic :: Utilities",
    ],
    python_requires=">=3.6",
    packages=find_packages(exclude=["tests"]),
    include_package_data=True,
    # All data files matched by MANIFEST.in will get included
    # if they are inside a package directory.
    zip_safe=False,
)
