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

for s in ["e\u0301le\u0300ve", "Z̷̳̎a̸̛ͅl̷̻̇g̵͉̉o̸̰͒", "기운찰만하다"]:
    egc = EGC(s)
    print(f"{len(s):>2}, {len(egc)}: {egc}")

# Output
#  7, 5: ['é', 'l', 'è', 'v', 'e']
# 20, 5: ['Z̷̳̎', 'a̸̛ͅ', 'l̷̻̇', 'g̵͉̉', 'o̸̰͒']
# 15, 6: ['기', '운', '찰', '만', '하', '다']


s = "ai\u0302ne\u0301e"  # aînée
print("".join(reversed(s)))
print("".join(reversed(EGC(s))))

# Output
# éen̂ia -> wrong (diacritics are messed up)
# eénîa -> right (regardless of the Unicode normalization form)
```

### Related resources
This implementation is based on the following resources:
- [“Grapheme Clusters”, in the Unicode core specification, version&nbsp;15.1.0](https://www.unicode.org/versions/Unicode15.1.0/ch03.pdf#G52443)
- [Unicode Standard Annex #29: Unicode Text Segmentation, version&nbsp;43](https://www.unicode.org/reports/tr29/tr29-43.html)

### Licenses
The code is available under the [MIT license](https://github.com/mlodewijck/pyuegc/blob/main/LICENSE).

Usage of Unicode data files is governed by the [UNICODE TERMS OF USE](https://www.unicode.org/copyright.html). Further specifications of rights and restrictions pertaining to the use of the Unicode data files and software can be found in the [Unicode Data Files and Software License](https://www.unicode.org/license.txt), a copy of which is included as [UNICODE-LICENSE](https://github.com/mlodewijck/pyunormalize/blob/master/UNICODE-LICENSE).
