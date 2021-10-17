# pyuegc
[![PyPI Version](https://img.shields.io/pypi/v/pyuegc.svg)](https://pypi.python.org/pypi/pyuegc) [![PyPI License](https://img.shields.io/pypi/l/pyuegc.svg)](https://pypi.python.org/pypi/pyuegc)

An implementation of the Unicode algorithm for breaking strings of text (i.e., code point sequences) into **extended grapheme clusters** (“user-perceived characters”) as specified in UAX #29, “Unicode Text Segmentation”. This package supports version&nbsp;14.0 of the Unicode Standard (released September&nbsp;14, 2021). It has been successfully tested against the [Unicode test file](https://www.unicode.org/Public/14.0.0/ucd/auxiliary/GraphemeBreakTest.txt).

### Installation
```shell
pip install pyuegc
```

### UCD version

To get the version of the Unicode character database currently used:
```python
>>> from pyuegc import UCD_VERSION
>>> UCD_VERSION
'14.0.0'
```

### Example usage
```python
from pyuegc import EGC

for s in ["e\u0301le\u0300ve", "Z̷̳̎a̸̛ͅl̷̻̇g̵͉̉o̸̰͒", "기운찰만하다"]:
    egc = EGC(s)
    print(f"{len(s):>2}, {len(egc)}: {egc}")

#  7, 5: ['é', 'l', 'è', 'v', 'e']
# 20, 5: ['Z̷̳̎', 'a̸̛ͅ', 'l̷̻̇', 'g̵͉̉', 'o̸̰͒']
# 15, 6: ['기', '운', '찰', '만', '하', '다']


s = "ai\u0302ne\u0301e"  # aînée
print("".join(reversed(s)))
print("".join(reversed(EGC(s))))

# éen̂ia -> wrong (diacritics are messed up)
# eénîa -> right (regardless of the Unicode normalization form)
```

### References
* https://www.unicode.org/versions/Unicode14.0.0/ch03.pdf#G52443
* https://unicode.org/reports/tr29/
* https://www.unicode.org/Public/14.0.0/ucd/auxiliary/GraphemeBreakProperty.txt
* https://www.unicode.org/Public/14.0.0/ucd/emoji/emoji-data.txt
* https://www.unicode.org/Public/14.0.0/ucd/auxiliary/GraphemeBreakTest.html
* https://www.unicode.org/Public/14.0.0/ucd/auxiliary/GraphemeBreakTest.txt

### Licenses
The pyuegc library is released under an [MIT license](https://github.com/mlodewijck/pyuegc/blob/master/LICENSE).

Usage of Unicode data files is governed by the [Unicode Terms of Use](https://www.unicode.org/copyright.html), a copy of which is included as [UNICODE-LICENSE](https://github.com/mlodewijck/pyuegc/blob/master/UNICODE-LICENSE).
