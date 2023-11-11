"""Unicode conformance testing.

- https://www.unicode.org/Public/15.1.0/ucd/auxiliary/GraphemeBreakTest.html
- https://www.unicode.org/Public/15.1.0/ucd/auxiliary/GraphemeBreakTest.txt
- https://www.unicode.org/reports/tr29/tr29-43.html
"""

import pathlib
import unittest

from pyuegc import EGC, UNICODE_VERSION

# Unicode conformance test file
UNICODE_FILE = "GraphemeBreakTest.txt"


def parse_file():
    records = []

    path = pathlib.Path.cwd() / "data" / UNICODE_FILE
    with path.open(encoding="utf-8") as f:
        assert UNICODE_VERSION in f.readline(), "Wrong Unicode version number."
        f.seek(0)

        for num, line in enumerate(f, 1):
            if "#" in line:
                pattern = line.split("#", 1)[0].rstrip()
            if not pattern:
                continue

            positions = []
            chars = []

            index = 0
            for x in pattern.split():
                # ÷ wherever there is a break opportunity
                # × wherever there is not
                if x == "÷":
                    positions.append(index)
                elif x != "×":
                    chars.append(chr(int(x, 16)))
                    index += 1

            string = "".join(chars)

            if len(positions) == 2:
                egc = [string]
            else:
                egc = [
                    string[i:j]
                    for i, j in zip(positions, positions[1:])
                ]

            records.append((num, string, egc))

    return records


def make_function(observed, expected):
    def ghost(self):
        self.assertEqual(observed, expected)
    return ghost


class TestExtendedGraphemeClusters(unittest.TestCase):
    pass


def generator():
    for num, string, expected in parse_file():
        testname = f"test_line_{num:04d}"
        observed = EGC(string)
        testfunc = make_function(observed, expected)
        setattr(TestExtendedGraphemeClusters, testname, testfunc)


generator()


if __name__ == "__main__":
    unittest.main()
