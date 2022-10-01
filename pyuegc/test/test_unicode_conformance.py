"""Unicode conformance testing.

- https://www.unicode.org/Public/15.0.0/ucd/auxiliary/GraphemeBreakTest.html
- https://www.unicode.org/Public/15.0.0/ucd/auxiliary/GraphemeBreakTest.txt
- https://www.unicode.org/reports/tr29/tr29-41.html
"""

import pathlib
import time
import unittest

from pyuegc import EGC, UNICODE_VERSION

# Unicode conformance test file
UNICODE_FILE = "GraphemeBreakTest.txt"


def parse_file():
    records = []

#   path = pathlib.Path(__file__).parent / "data" / UNICODE_FILE
    path = pathlib.Path.cwd() / "data" / UNICODE_FILE
    with path.open(encoding="utf-8") as f:
        assert UNICODE_VERSION in f.readline(), "Wrong Unicode version number."
        f.seek(0)

        for num, line in enumerate(f, 1):
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
