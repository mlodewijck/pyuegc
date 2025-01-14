"""Unit tests for pyuegc."""

import os
import unittest

from pyuegc import EGC, UNICODE_VERSION as _UNICODE_VERSION

UNICODE_VERSION = "16.0.0"
assert UNICODE_VERSION == _UNICODE_VERSION, "Wrong Unicode version number."

# Test data available at https://www.unicode.org/cldr/cldr-aux/production/common/testData/segmentation/graphemeCluster/
FILES = (
    "TestSegmenter-Bengali.txt",
    "TestSegmenter-Devanagari.txt",
    "TestSegmenter-Gujarati.txt",
    "TestSegmenter-Malayalam.txt",
    "TestSegmenter-Odia.txt",
    "TestSegmenter-Telugu.txt",
)


def parse_file(filename):
    records = []

    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, "data")
    path = os.path.join(data_dir, filename)

    with open(path, encoding="utf-8-sig") as f:
        for num, line in enumerate(f, 1):
            line = line.replace(" ", "").strip()

            if not line or line.startswith("#"):
                continue

            string, _, expected = line.partition(";")
            expected = expected.strip("÷").split("÷")
            records.append((num, string, expected))

    return records


def make_function(observed, expected):
    def ghost(self):
        self.assertEqual(observed, expected)
    return ghost


class TestExtendedGraphemeClusters(unittest.TestCase):
    pass


def generator():
    for filename in FILES:
        script = filename[:-4].split("-")[1]
        for num, string, expected in parse_file(filename):
            testname = f"test_{script}_line_{num:03d}"
            observed = EGC(string)
            testfunc = make_function(observed, expected)
            setattr(TestExtendedGraphemeClusters, testname, testfunc)


generator()


if __name__ == "__main__":
    unittest.main()
