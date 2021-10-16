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
>>> from pyuegc import EGC
>>> len("e\u0301le\u0300ve")
7
>>> len(EGC("e\u0301le\u0300ve"))
5
>>> EGC("e\u0301le\u0300ve")
['é', 'l', 'è', 'v', 'e']
>>>
>>> s = "Z̸͕̪̆᷾᷾︣̌͊̕͝a̸̛͎ͭ͛̉᷆̿̂̚l̸̨̧̛̹̪̦̞̳ͧͬ̈́̽͜ǵ̶̢̛͓᷿̼̱̗̳̏︠o̵̘͓̣͚̍̎͆ͣ︡̓̓̅͠"
>>> len(s)
67
>>> clusters = EGC(s)
>>> clusters
['Z̸͕̪̆᷾᷾︣̌͊̕͝', 'a̸̛͎ͭ͛̉᷆̿̂̚', 'l̸̨̧̛̹̪̦̞̳ͧͬ̈́̽͜', 'ǵ̶̢̛͓᷿̼̱̗̳̏︠', 'o̵̘͓̣͚̍̎͆ͣ︡̓̓̅͠']
>>> len(clusters)
5
>>> s[:2]
'Z̆'
>>> "".join(clusters[:2])
'Z̸͕̪̆᷾᷾︣̌͊̕͝a̸̛͎ͭ͛̉᷆̿̂̚'
>>> 
>>> s = "기운찰만하다"
>>> len(s)
15
>>> clusters = EGC(s)
>>> clusters
['기', '운', '찰', '만', '하', '다']
>>> len(clusters)
6
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
