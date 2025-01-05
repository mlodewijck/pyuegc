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
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Software Development",
        "Topic :: Software Development :: Internationalization",
        "Topic :: Software Development :: Localization",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing",
        "Topic :: Utilities",
    ],
    python_requires=">=3.8",
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    include_package_data=True,
    zip_safe=False,
)
