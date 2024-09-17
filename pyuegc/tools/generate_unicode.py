# This script generates the pyuegc.unicode module.
#
# Input files:
#     https://www.unicode.org/Public/16.0.0/ucd/auxiliary/GraphemeBreakProperty.txt
#     https://www.unicode.org/Public/16.0.0/ucd/emoji/emoji-data.txt
#     https://www.unicode.org/Public/16.0.0/ucd/IndicSyllabicCategory.txt
#     https://www.unicode.org/Public/16.0.0/ucd/UnicodeData.txt
#
# Output file:
#     tools/generate_unicode/unicode.py
#
# The output file must be copied to the `pyuegc` directory.

import pathlib
import urllib.error
import urllib.request

UNICODE_VERSION = "16.0.0"
SCRIPT_PATH = "/".join(pathlib.Path(__file__).parts[-3:])

# Files from the Unicode character database (UCD)
UNICODE_EMOJI = "emoji-data.txt"
UNICODE_GBP   = "GraphemeBreakProperty.txt"
UNICODE_INDIC = "IndicSyllabicCategory.txt"
UNICODE_UDATA = "UnicodeData.txt"


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

    print(f".. Extracting data from {filename}")
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

    gcb_prop_list = []
    extend_list = []  # needed later
    zwj_list = []     # needed later

    for item in lines:
        item = item.rstrip()

        if item.startswith("#") or not item:
            continue

        data = item.split("#")[0].split(";")
        prop = data[1].strip()

        for code in codepoint_range(data[0].strip()):
            code = f"{code:04X}"
            gcb_prop_list.append(f'    0x{code:0>5}: "{prop}",')

            if prop == "Extend":
                extend_list.append(code)
            elif prop == "ZWJ":
                zwj_list.append(code)

    #
    # Unicode file: emoji-data.txt
    #

    try:
        lines = (cwd / UNICODE_EMOJI).read_text(encoding="utf-8").splitlines()
    except FileNotFoundError:
        lines = read_remote(f"emoji/{UNICODE_EMOJI}")
        print(".. Done.")

    ext_pict_list = []
    # \p{Extended_Pictographic}
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
            ext_pict_list.append(
                f'    *range(0x{start:0>5}, 0x{end:0>5} + 1),'
            )
        else:
            ext_pict_list.append(f"           0x{item:0>5},")

    #
    # Unicode file: IndicSyllabicCategory.txt
    #

    try:
        lines = (cwd / UNICODE_INDIC).read_text(encoding="utf-8").splitlines()
    except FileNotFoundError:
        lines = read_remote(UNICODE_INDIC)
        print(".. Done.")

    # Check file version
    assert UNICODE_VERSION in lines[0], "Wrong Unicode version number."

    linking_consonants_list = []
    # [
    # \p{Gujr}\p{sc=Telu}\p{sc=Mlym}\p{sc=Orya}\p{sc=Beng}\p{sc=Deva}
    # & \p{Indic_Syllabic_Category=Consonant}
    # ]
    start = lines.index("# Indic_Syllabic_Category=Consonant")
    stop  = lines.index("# Indic_Syllabic_Category=Consonant_Dead")

    for line in lines[start:stop]:
        line = line.rstrip()

        if line and not line.startswith('#'):
            if ("BENGALI" in line
                    or "DEVANAGARI" in line
                    or "GUJARATI" in line
                    or "MALAYALAM" in line
                    or "ORIYA" in line
                    or "TELUGU" in line
            ):
                code, rest = line.split(";")
                code = code.rstrip()
                if ".." in code:
                    start, end = code.split("..")
                    linking_consonants_list.append(
                        f"    *range(0x{start:0>5}, 0x{end:0>5} + 1),"
                        f"  # {rest[22:]}")
                else:
                    linking_consonants_list.append(
                        f"           0x{code:0>5},  {12 * ' '}"
                        f"  # {rest[22:]}")

    conjunct_linkers_list = []
    # [
    # \p{Gujr}\p{sc=Telu}\p{sc=Mlym}\p{sc=Orya}\p{sc=Beng}\p{sc=Deva}
    # & \p{Indic_Syllabic_Category=Virama}
    # ]
    start = lines.index("# Indic_Syllabic_Category=Virama")
    stop  = lines.index("# Indic_Syllabic_Category=Pure_Killer")

    for line in lines[start:stop]:
        line = line.rstrip()

        if line and not line.startswith('#'):
            if ("BENGALI" in line
                    or "DEVANAGARI" in line
                    or "GUJARATI" in line
                    or "MALAYALAM" in line
                    or "ORIYA" in line
                    or "TELUGU" in line
            ):
                code, rest = line.split(";")
                code = code.rstrip()
                if ".." in code:
                    start, end = code.split("..")
                    conjunct_linkers_list.append(
                        f"    *range(0x{start:0>5}, 0x{end:0>5} + 1),"
                        f"  # {rest[19:]}")
                else:
                    conjunct_linkers_list.append(
                        f"    0x{code:0>5},  # {rest[19:]}")

    #
    # Unicode file: UnicodeData.txt
    #

    try:
        lines = (cwd / UNICODE_UDATA).read_text(encoding="utf-8").splitlines()
    except FileNotFoundError:
        lines = read_remote(UNICODE_UDATA)
        print(".. Done.")

    ext_ccc_zwj_list = []
    # [[Extend-\p{ccc=0}] $ZWJ]
    extend = set(extend_list)

    for item in lines:
        items = item.split(";", 4)
        code = items[0]
        if code in extend and items[3] != "0":
            ext_ccc_zwj_list.append(f"    0x{code:0>5},")

    for code in zwj_list:
        ext_ccc_zwj_list.append(f"    0x{code:0>5},")


    gcb_prop = "\n".join(gcb_prop_list)
    ext_pict = "\n".join(ext_pict_list)
    linking_consonants = "\n".join(linking_consonants_list)
    conjunct_linkers = "\n".join(conjunct_linkers_list)
    ext_ccc_zwj = "\n".join(ext_ccc_zwj_list)

    with open(cwd / "_unicode.py", "w", encoding="utf-8", newline="\n") as f:
        f.write(f'''\
"""Data derived from the Unicode character database (UCD).

This file was generated from {SCRIPT_PATH}
"""

_UNICODE_VERSION = "{UNICODE_VERSION}"

# Mapping of Unicode code points to their corresponding grapheme cluster
# break property values (any code point not explicitly listed here defaults
# to "Other")
_PROP_DICT = {{
{gcb_prop}
}}

# List of Unicode code points that have the Extended_Pictographic property
_EXT_PICT = [
{ext_pict}
]

# [\\p{{Gujr}}\\p{{sc=Telu}}\\p{{sc=Mlym}}\\p{{sc=Orya}}\\p{{sc=Beng}}\\p{{sc=Deva}}
# & \\p{{Indic_Syllabic_Category=Consonant}}]
_LINKING_CONSONANTS = "".join(map(chr, [
{linking_consonants}
]))

# [\\p{{Gujr}}\\p{{sc=Telu}}\\p{{sc=Mlym}}\\p{{sc=Orya}}\\p{{sc=Beng}}\\p{{sc=Deva}}
# & \\p{{Indic_Syllabic_Category=Virama}}]
_CONJUNCT_LINKERS = "".join(map(chr, [
{conjunct_linkers}
]))

# [[Extend-\\p{{ccc=0}}] $ZWJ]
_EXT_CCC_ZWJ = "".join(map(chr, [
{ext_ccc_zwj}
]))
''')


if __name__ == "__main__":
    main()
