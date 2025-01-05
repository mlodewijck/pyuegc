"""Utility for listing Unicode default extended grapheme clusters.

This pure-Python package implements the Unicode algorithm for breaking strings
of text (i.e., code point sequences) into extended grapheme clusters ("user-
perceived characters"). It adheres to the Unicode standard version 16.0,
released in September 2024.

Copyright (c) 2021-2025, Marc Lodewijck
All rights reserved.

This software is distributed under the MIT license.
"""

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
