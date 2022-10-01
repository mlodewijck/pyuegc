# This script generates the pyuegc.unicode module.
#
# Input files:
#     https://www.unicode.org/Public/15.0.0/ucd/auxiliary/GraphemeBreakProperty.txt
#     https://www.unicode.org/Public/15.0.0/ucd/emoji/emoji-data.txt
#
# Output file:
#     tools/generate_unicode/unicode.py
#
# The output file must be copied to the *pyuegc* directory.

import pathlib
import urllib.error
import urllib.request

UNICODE_VERSION = "15.0.0"
SCRIPT_PATH = "/".join(pathlib.Path(__file__).parts[-3:])

# Files from the Unicode character database (UCD)
UNICODE_EMOJI = "emoji-data.txt"
UNICODE_GBP = "GraphemeBreakProperty.txt"


def read_remote(filename):
    url = f"https://www.unicode.org/Public/{UNICODE_VERSION}/ucd/"
    try:
        print("\n.. Fetching URL...")
        response = urllib.request.urlopen(f"{url}{filename}")
        # print(response.__dict__)
    except urllib.error.HTTPError as e:
        raise Exception(
            f"The server could not fulfill the request. Error code: {e.code}"
        )
    except urllib.error.URLError as e:
        raise Exception(
            f"We failed to reach a server.\nReason:\n{e.reason}"
        )

    print(".. Extracting data...")
    return response.read().decode("utf-8").splitlines()


def codepoint_range(data, separator=".."):
    if separator in data:
        start, end = data.split(separator)
    else:
        start = end = data
    return range(int(start, 16), int(end, 16) + 1)


def main():
    # Current working directory
    cwd = pathlib.Path.cwd()

    #
    # Unicode file: GraphemeBreakProperty.txt
    #

    try:
        lines = (cwd / UNICODE_GBP).read_text(encoding="utf-8").splitlines()
    except FileNotFoundError:
        lines = read_remote(f"auxiliary/{UNICODE_GBP}")
        print(".. Done.")

    # Check file version
    assert UNICODE_VERSION in lines[0], "Wrong Unicode version number."

    gcb_list = []
    for item in lines:
        item = item.rstrip()
        if item.startswith("#") or not item:
            continue
        data = item.split("#")[0].split(";")
        prop = data[1].strip()
        for code in codepoint_range(data[0].strip()):
            code = f"{code:04X}"
            gcb_list.append(f'    0x{code:0>5}: "{prop}",')

    #
    # Unicode file: emoji-data.txt
    #

    try:
        lines = (cwd / UNICODE_EMOJI).read_text(encoding="utf-8").splitlines()
    except FileNotFoundError:
        lines = read_remote(f"emoji/{UNICODE_EMOJI}")
        print(".. Done.")

    ext_pictogr_list = []
    for item in lines:
        item = item.rstrip()
        if item.startswith("# Used with Emoji Version"):
            # Check file version
            assert UNICODE_VERSION[:-2] in item, \
                "Wrong Unicode version number."
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


    gcb = "\n".join(gcb_list)
    ext_pictogr = "\n".join(ext_pictogr_list)

    with open(cwd / "unicode.py", "w", encoding="utf-8", newline="\n") as f:
        f.write(f'''\
"""Data derived from the Unicode character database (UCD).

This file was generated from {SCRIPT_PATH}
"""

UNICODE_VERSION = "{UNICODE_VERSION}"

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
