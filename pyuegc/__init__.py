"""Utility for listing Unicode default extended grapheme clusters.

This Python library implements the Unicode text segmentation algorithm,
accurately segmenting Unicode text (code point sequences) into a list
of their constituent extended grapheme clusters. It adheres to the Unicode
standard version 16.0 (released in September 2024) and has been rigorously
tested using the official Unicode test file available at
https://www.unicode.org/Public/16.0.0/ucd/auxiliary/GraphemeBreakTest.txt.

For the formal specification of Unicode text segmentation algorithms,
refer to Unicode Standard Annex #29, "Unicode Text Segmentation,"
at https://www.unicode.org/reports/tr29/tr29-45.html.

Copyright (c) 2021-2024, Marc Lodewijck
All rights reserved.

This software is distributed under the MIT license.
"""

import sys

if sys.version_info < (3, 6):
    raise SystemExit(f"\n{__package__} requires Python 3.6 or later.")
del sys

__all__ = [
    "EGC",
    "UCD_VERSION",
    "UNICODE_VERSION",
    "__version__",
]

# Unicode standard used to process the data
UNICODE_VERSION = UCD_VERSION = "16.0.0"


from pyuegc import _version
__version__ = _version.__version__
del _version

from pyuegc._unicode import _UNICODE_VERSION
if _UNICODE_VERSION != UNICODE_VERSION:
    raise SystemExit(
        f"Unicode version mismatch in {_unicode.__name__} "
        f"(expected {UNICODE_VERSION}, found {_UNICODE_VERSION})."
    )
del _UNICODE_VERSION

from pyuegc.egc import EGC
