import os.path
import re

# The Unicode Standard used to process the data
UNICODE_VERSION = "14.0.0"

# The Unicode Character Database
UCD_VERSION = UNICODE_VERSION

# Files from the UCD
UNICODE_EMO = "emoji-data.txt"
UNICODE_GBP = "GraphemeBreakProperty.txt"


def _codepoint_range(data, separator=".."):
    if separator in data:
        start, end = data.split(separator)
    else:
        start = end = data
    return range(int(start, 16), int(end, 16) + 1)


def main():
    dir_path = os.path.dirname(__file__)

    #
    # Unicode file: GraphemeBreakProperty.txt
    #

    path = os.path.join(dir_path, UNICODE_GBP)
    with open(path, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()

    # Check file version
    assert re.match(
        "^#.*{}-(.+).txt.*$".format(UNICODE_GBP[:-4]), lines[0]
    ).group(1) == UCD_VERSION

    gcb_list = []
    for item in lines:
        item = item.rstrip()
        if item.startswith("#") or not item:
            continue
        data = item.split("#")[0].split(";")
        prop = data[1].strip()
        for code in _codepoint_range(data[0].strip()):
            code = f"{code:04X}"
            gcb_list.append(f'    0x{code:0>5}: "{prop}",')

    #
    # Unicode file: emoji-data.txt
    #

    path = os.path.join(dir_path, UNICODE_EMO)
    with open(path, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()

    ext_pictogr_list = []
    for item in lines:
        item = item.rstrip()
        if item.startswith("# Version:"):
            # Check file version
            assert re.match(
                "^#.*Version:\s(.+)$".format(UNICODE_EMO[:-4]), item
            ).group(1) == UCD_VERSION[:-2]
        elif item.startswith('#') or not item:
            continue
        if not "Extended_Pictographic" in item:
            continue
        item = item.split(";")[0].rstrip()
        if ".." in item:
            start, end = item.split("..")
            ext_pictogr_list.append(
                f'    *range(0x{start:0>5}, 0x{end:0>5} + 1),'
            )
        else:
            ext_pictogr_list.append(f"    0x{item:0>5},")


    filename = os.path.basename(__file__).split("_", 1)[1]

    gcb = "\n".join(gcb_list)
    ext_pictogr = "\n".join(ext_pictogr_list)

    with open(filename, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write(f'''\
"""Data derived from the Unicode Character Database."""

UCD_VERSION = "{UCD_VERSION}"

# Grapheme cluster break property values
# All code points not explicitly listed for Grapheme_Cluster_Break
# have the value "Other"
_GCB_PROP_VAL = {{
{gcb}
}}

# Extended pictographic characters
# All the code points that have the Extended_Pictographic property
_EXT_PICTOGR = [
{ext_pictogr}
]
''')


if __name__ == '__main__':
    main()
