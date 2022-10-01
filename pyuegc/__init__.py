"""A python implementation of the Unicode algorithm for breaking strings
of text (i.e., code point sequences) into extended grapheme clusters. This
package supports version 15.0 of the Unicode standard (September 13, 2022).
It has been thoroughly tested against the Unicode test file found
at https://www.unicode.org/Public/15.0.0/ucd/auxiliary/GraphemeBreakTest.txt

To get the version of the Unicode character database currently used:

    >>> from pyuegc import UCD_VERSION
    >>> UCD_VERSION
    '15.0.0'

For the formal specification, see Unicode Standard Annex #29, "Unicode Text
Segmentation", at https://www.unicode.org/reports/tr29/tr29-41.html
"""

import sys
if sys.version_info < (3, 6):
    raise SystemExit(f"\n{__package__.title()} requires Python 3.6 or later.")
del sys

__all__ = [
    "EGC",
    "UCD_VERSION",
    "UNICODE_VERSION",
    "__version__",
]

# Unicode standard used to process the data
# Version released on September 13, 2022
UNICODE_VERSION = UCD_VERSION = "15.0.0"


from pyuegc import _version
__version__ = _version.__version__
del _version

from pyuegc.unicode import UNICODE_VERSION as _UNICODE
if _UNICODE != UNICODE_VERSION:
    raise SystemExit(f"\nWrong Unicode version number in {unicode.__name__}")

from pyuegc.egc import EGC
