# This script generates the pyuegc._unicode module.
#
# Input files:
#     https://www.unicode.org/Public/16.0.0/ucd/auxiliary/GraphemeBreakProperty.txt
#     https://www.unicode.org/Public/16.0.0/ucd/emoji/emoji-data.txt
#     https://www.unicode.org/Public/16.0.0/ucd/DerivedCoreProperties.txt
#
# Output file:
#     tools/generate_unicode/_unicode.py
#
# The output file must be copied to the `pyuegc` directory.

import pathlib
import urllib.error
import urllib.request

UNICODE_VERSION = "16.0.0"
SCRIPT_PATH = "/".join(pathlib.Path(__file__).parts[-3:])

# Files from the Unicode character database (UCD)
DERIVED_CORE_PROPERTIES = "DerivedCoreProperties.txt"
EMOJI_DATA = "emoji-data.txt"
GRAPHEME_BREAK_PROPRETY = "GraphemeBreakProperty.txt"


def read_remote(filename):
    base_url = f"https://www.unicode.org/Public/{UNICODE_VERSION}/ucd/"
    url = f"{base_url}{filename}"

    try:
        print("\n.. Fetching URL...")
        with urllib.request.urlopen(url) as response:
            print(f".. Extracting data from {filename}")
            return response.read().decode("utf-8").splitlines()
    except urllib.error.HTTPError as e:
        raise Exception(
            f"HTTPError: Could not fulfill the request. Error code: {e.code}"
        )
    except urllib.error.URLError as e:
        raise Exception(
            f"URLError: Failed to reach the server. Reason: {e.reason}"
        )


def parse_lines(lines, target_property=None):
    results = []
    property_data = {}

    code_points = set()
    total_points_expected = None

    wanted = ("# Total code points:", "# Total elements:")

    for line in lines:
        if not line or (line.startswith("#") and not line.startswith(wanted)):
            continue

        if line.startswith(wanted):
            total_points_expected = int(line.split(":")[1].strip())

            if curr_prop:
                property_data[curr_prop] = {
                    "code_points": code_points,
                    "total_expected": total_points_expected,
                    "total_actual": len(code_points),
                    "match": len(code_points) == total_points_expected,
                }

            curr_prop = None
            code_points = set()
            total_points_expected = None

        else:
            parts = line.split(";", 1)
            data = parts[0].strip()
            curr_prop = parts[1].split("#")[0].strip()

            if target_property and curr_prop != target_property:
                continue

            if ".." in data:
                start, end = [int(cp, 16) for cp in data.split("..")]
                code_points.update([*range(start, end + 1)])

                if target_property is None:
                    for code in range(start, end + 1):
                        results.append(f'    0x{code:05X}: "{curr_prop}",')
                else:
                    results.append(
                        f"    *range(0x{start:05X}, 0x{end:05X} + 1),"
                    )

            else:
                code_points.add(data)

                if target_property is None:
                    results.append(f'    0x{data:0>5}: "{curr_prop}",')
                else:
                    indent = \
                        " " * (4 if target_property == "InCB; Linker" else 11)
                    results.append(f"{indent}0x{data:0>5},")

    for prop, data in property_data.items():
        if target_property and prop != target_property:
            continue
        print()
        print(f"Property: {prop}")
        print(f"  Expected:  {data['total_expected']:>6,} code points")
        print(f"  Collected: {data['total_actual']:>6,} code points")
        assert data["match"]

    return results


def main():
    # Current working directory
    cwd = pathlib.Path.cwd()


    #
    # Unicode file: GraphemeBreakProperty.txt
    #

    try:
        lines = (cwd / GRAPHEME_BREAK_PROPRETY).read_text(encoding="utf-8").splitlines()
    except FileNotFoundError:
        lines = read_remote(f"auxiliary/{GRAPHEME_BREAK_PROPRETY}")
        print(".. Done.")

    assert UNICODE_VERSION in lines[0], "Unicode version mismatch"

    # Grapheme_Cluster_Break property values
    gcb_prop_values = parse_lines(lines)


    #
    # Unicode file: emoji-data.txt
    #

    try:
        lines = (cwd / EMOJI_DATA).read_text(encoding="utf-8").splitlines()
    except FileNotFoundError:
        lines = read_remote(f"emoji/{EMOJI_DATA}")
        print(".. Done.")

    # [\p{Extended_Pictographic}]
    ExtendedPictographic = \
        parse_lines(lines, target_property="Extended_Pictographic")


    #
    # Unicode file: DerivedCoreProperties.txt
    #

    # Indic sequences
    #   InCBLinker    = [\p{InCB=Linker}]
    #   InCBConsonant = [\p{InCB=Consonant}]
    #   InCBExtend    = [\p{InCB=Extend}]

    try:
        lines = (cwd / DERIVED_CORE_PROPERTIES).read_text(encoding="utf-8").splitlines()
    except FileNotFoundError:
        lines = read_remote(DERIVED_CORE_PROPERTIES)
        print(".. Done.")

    assert UNICODE_VERSION in lines[0], "Unicode version mismatch"

    # [\p{InCB=Consonant}]
    # https://www.unicode.org/reports/tr44/tr44-34.html#Indic_Conjunct_Break
    #   InCB = Consonant iff C in [S &\p{Indic_Syllabic_Category=Consonant}]
    #   S = [\p{sc=Beng}\p{sc=Deva}\p{sc=Gujr}\p{sc=Mlym}\p{sc=Orya}\p{sc=Telu}]
    InCBConsonant = parse_lines(lines, target_property="InCB; Consonant")

    # [\p{InCB=Linker}]
    # https://www.unicode.org/reports/tr44/tr44-34.html#Indic_Conjunct_Break
    #   InCB = Linker iff C in [S &\p{Indic_Syllabic_Category=Virama}]
    #   S = [\p{sc=Beng}\p{sc=Deva}\p{sc=Gujr}\p{sc=Mlym}\p{sc=Orya}\p{sc=Telu}]
    InCBLinker = parse_lines(lines, target_property="InCB; Linker")

    # [\p{InCB=Extend}]
    # https://www.unicode.org/reports/tr44/tr44-34.html#Indic_Conjunct_Break
    #   InCB = Extend iff C in [
    #       \p{gcb=Extend}
    #       \p{gcb=ZWJ}
    #       -\p{InCB=Linker}
    #       -\p{InCB=Consonant}
    #       -[\u200C]
    #   ]
    InCBExtend = parse_lines(lines, target_property="InCB; Extend")


    PROP_DICT = "\n".join(gcb_prop_values)
    EXT_PICTOGR = "\n".join(ExtendedPictographic)
    INCB_CONSONANT = "\n".join(InCBConsonant)
    INCB_LINKER = "\n".join(InCBLinker)
    INCB_EXTEND = "\n".join(InCBExtend)

    with open(cwd / "_unicode.py", "w", encoding="utf-8", newline="\n") as f:
        f.write(f'''\
"""Data derived from the Unicode character database (UCD).

This file was generated from {SCRIPT_PATH}
"""

_UNICODE_VERSION = "{UNICODE_VERSION}"

# Mapping of Unicode code points to their corresponding grapheme cluster
# break property values (any code point not listed here defaults to "Other")
# Source: GraphemeBreakProperty.txt
_PROP_DICT = {{
{PROP_DICT}
}}

# [\\p{{Extended_Pictographic}}]
# Source: emoji-data.txt
_EXT_PICTOGR = [
{EXT_PICTOGR}
]

# [\\p{{InCB=Consonant}}]
# Source: DerivedCoreProperties.txt
_INCB_CONSONANT = "".join(map(chr, [
{INCB_CONSONANT}
]))

# [\\p{{InCB=Linker}}]
# Source: DerivedCoreProperties.txt
_INCB_LINKER = "".join(map(chr, [
{INCB_LINKER}
]))

# [\\p{{InCB=Extend}}]
# Source: DerivedCoreProperties.txt
_INCB_EXTEND = "".join(map(chr, [
{INCB_EXTEND}
]))
''')


if __name__ == "__main__":
    main()
