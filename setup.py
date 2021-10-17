from setuptools import setup, find_packages

from pyuegc import __version__, UNICODE_VERSION

URL = "https://github.com/mlodewijck/pyuegc"

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pyuegc",
    version=__version__,
    description=(
        "An implementation of the Unicode algorithm for breaking code point "
        "sequences into extended grapheme clusters as specified in UAX #29. "
        "This library supports version {} of the Unicode Standard."
        .format(UNICODE_VERSION[:-2])
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=URL,
    author="Marc Lodewijck",
    author_email="mlodewijck@gmail.com",
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "Topic :: Software Development",
        "Topic :: Software Development :: Internationalization",
        "Topic :: Text Processing",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    keywords=[
        "Unicode",
        "Unicode grapheme clusters",
        "extended grapheme cluster",
        "EGC",
        "grapheme cluster",
        "graphemes",
        "segmentation",
    ],
    python_requires=">=3.6",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    project_urls={
        "Bug Reports": "{}/issues".format(URL),
        "Source": "{}/".format(URL),
    },
)
