"""Unicode conformance testing.

- www.unicode.org/Public/14.0.0/ucd/auxiliary/GraphemeBreakTest.html
- www.unicode.org/Public/14.0.0/ucd/auxiliary/GraphemeBreakTest.txt
- unicode.org/reports/tr29/
"""

import os.path as _p
import re
import unittest

from pyuegc import EGC

# The Unicode Standard used to process the data
UNICODE_VERSION = "14.0.0"

# The Unicode Character Database
UCD_VERSION = UNICODE_VERSION

# File from the UCD
UNICODE_FILE = "GraphemeBreakTest.txt"


def parse_file():
    records = []

    path = _p.join(_p.dirname(__file__), UNICODE_FILE)
    with open(path, "r", encoding="utf-8") as fh:
        assert re.match(
            f"^#\s*{UNICODE_FILE[:-4]}-(.+)\.txt.*$", fh.readline()
        ).group(1) == UCD_VERSION, "Wrong UCD version number."

        fh.seek(0)

        for num, line in enumerate(fh, 1):
            if "#" in line:
                pattern = line.split("#", 1)[0].rstrip()
            if not pattern:
                continue

            cp = []
            breakpoints = []
            cp_count = 0
            for x in pattern.split():
                # ÷ wherever there is a break opportunity
                # × wherever there is not
                if x == "÷":
                    breakpoints.append(cp_count)
                elif x == "×":
                    pass
                else:
                    cp.append(chr(int(x, 16)))
                    cp_count += 1

            string = "".join(cp)
            graphemes = [
                string[i:j]
                for i, j in zip(breakpoints, breakpoints[1:])
            ]
            records.append([num, string, graphemes])

    return records


def make_function(observed, expected):
    def ghost(self):
        self.assertEqual(observed, expected)
    return ghost


class TestExtendedGraphemeClusters(unittest.TestCase):
    pass


def generator():
    for record in parse_file():
        testname = f"test_line_{record[0]:03d}"
        observed = EGC(record[1])
        expected = record[2]
        testfunc = make_function(observed, expected)
        setattr(TestExtendedGraphemeClusters, testname, testfunc)


generator()


if __name__ == "__main__":
    unittest.main()
