# pyuegc
An implementation of the Unicode algorithm for breaking strings of text (i.e., code point sequences) into **extended grapheme clusters** (“user-perceived characters”) as specified in UAX #29, “Unicode Text Segmentation”. This package supports version&nbsp;15.1 of the Unicode standard (released in September&nbsp;2023). It has been thoroughly tested against the [Unicode test file](https://www.unicode.org/Public/15.1.0/ucd/auxiliary/GraphemeBreakTest.txt).

### Installation
The easiest method to install is using pip:
```shell
pip install pyuegc
```

### UCD version
To get the version of the Unicode character database currently used:
```python
>>> from pyuegc import UCD_VERSION
>>> UCD_VERSION
'15.1.0'
```

### Example usage
```python
from pyuegc import EGC


def _output(unistr, egc):
    return f"""\
# String: {unistr}
# Length of string: {len(unistr)}
# EGC: {egc}
# Length of EGC: {len(egc)}
"""

unistr = "Python"
egc = EGC(unistr)
print(_output(unistr, egc))
# String: Python
# Length of string: 6
# EGC: ['P', 'y', 't', 'h', 'o', 'n']
# Length of EGC: 6

unistr = "e\u0301le\u0300ve"
egc = EGC(unistr)
print(_output(unistr, egc))
# String: élève
# Length of string: 7
# EGC: ['é', 'l', 'è', 'v', 'e']
# Length of EGC: 5

unistr = "Z̷̳̎a̸̛ͅl̷̻̇g̵͉̉o̸̰͒"
egc = EGC(unistr)
print(_output(unistr, egc))
# String: Z̷̳̎a̸̛ͅl̷̻̇g̵͉̉o̸̰͒
# Length of string: 20
# EGC: ['Z̷̳̎', 'a̸̛ͅ', 'l̷̻̇', 'g̵͉̉', 'o̸̰͒']
# Length of EGC: 5

unistr = "기운찰만하다"
egc = EGC(unistr)
print(_output(unistr, egc))
# String: 기운찰만하다
# Length of string: 15
# EGC: ['기', '운', '찰', '만', '하', '다']
# Length of EGC: 6

unistr = "পৌষসংক্রান্তির"
egc = EGC(unistr)
print(_output(unistr, egc))
# String: পৌষসংক্রান্তির
# Length of string: 14
# EGC: ['পৌ', 'ষ', 'সং', 'ক্রা', 'ন্তি', 'র']
# Length of EGC: 6


unistr = "ai\u0302ne\u0301e"  # aînée
print(f"# Reversed string:\n#   {''.join(reversed(unistr))}")
print(f"# Reversed EGC:   \n#   {''.join(reversed(EGC(unistr)))}")
# Reversed string:
#   éen̂ia -> wrong (diacritics are messed up)
# Reversed EGC:
#   eénîa -> right (regardless of the Unicode normalization form)
```

### Related resources
This implementation is based on the following resources:
- [“Grapheme Clusters”, in the Unicode core specification, version&nbsp;15.1.0](https://www.unicode.org/versions/Unicode15.1.0/ch03.pdf#G52443)
- [Unicode Standard Annex #29: Unicode Text Segmentation, version&nbsp;43](https://www.unicode.org/reports/tr29/tr29-43.html)

### Licenses
The code is available under the [MIT license](https://github.com/mlodewijck/pyuegc/blob/main/LICENSE).

Usage of Unicode data files is governed by the [UNICODE TERMS OF USE](https://www.unicode.org/copyright.html). Further specifications of rights and restrictions pertaining to the use of the Unicode data files and software can be found in the [Unicode Data Files and Software License](https://www.unicode.org/license.txt), a copy of which is included as [UNICODE-LICENSE](https://github.com/mlodewijck/pyunormalize/blob/master/UNICODE-LICENSE).
