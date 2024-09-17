"""Break Unicode strings into their default extended grapheme clusters.

This module provides the `EGC` function, which accurately splits a Unicode
string into its constituent extended grapheme clusters following the Unicode
standard.
"""

import re

from pyuegc._unicode import (
    _PROP_DICT,
    _EXT_PICT,
    _LINKING_CONSONANTS,
    _CONJUNCT_LINKERS,
    _EXT_CCC_ZWJ,
)

_PROP = {**_PROP_DICT, **dict.fromkeys(_EXT_PICT, "Extended_Pictographic")}

# Regular expression pattern object used to match certain
# conjunct linker clusters (Indic aksaras)
_RE_CONJUNCT_LINKER_CLUSTER = re.compile(
    f"   [ {_LINKING_CONSONANTS} ] "              # LinkingConsonant
    f"   [ {_EXT_CCC_ZWJ}        ]*"              # ExtCccZwj*
    f"   [ {_CONJUNCT_LINKERS}   ] "              # ConjunctLinker
    f"   [ {_EXT_CCC_ZWJ}        ]*"              # ExtCccZwj*
    f"(?=[ {_LINKING_CONSONANTS} ])", re.VERBOSE  # LinkingConsonant
)

del _PROP_DICT, _EXT_PICT, _LINKING_CONSONANTS, _CONJUNCT_LINKERS, _EXT_CCC_ZWJ

# Grapheme cluster break chart
# https://www.unicode.org/Public/16.0.0/ucd/auxiliary/GraphemeBreakTest.html
_GCB_CHART = [
    [1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0],  # Other
    [1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],  # CR
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],  # LF
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],  # Control
    [1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0],  # Extend
    [1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0],  # Regional_Indicator
    [0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Prepend
    [1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0],  # SpacingMark
    [1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0],  # L
    [1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0],  # V
    [1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0],  # T
    [1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0],  # LV
    [1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0],  # LVT
    [1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0],  # Extended_Pictographic
    [1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0],  # ZWJ
]

_GCB_VALUES = (
  # "Other",  # not a GCB property value (used to represent any code point)
    None,     # used in lieu of "Other"
    "CR",
    "LF",
    "Control",
    "Extend",
    "Regional_Indicator",
    "Prepend",
    "SpacingMark",
    "L",
    "V",
    "T",
    "LV",
    "LVT",
    "Extended_Pictographic",  # not a GCB property value
    "ZWJ",
)

_EXTEND = {
    "Extend",
    "Extended_Pictographic",
}


def _build_break_rules_set():
    break_rules_set = set()

    for i, sublist in enumerate(_GCB_CHART):
        for j, val in enumerate(sublist):
            if val:
                break_rules_set.add((_GCB_VALUES[i], _GCB_VALUES[j]))

    return break_rules_set


# Build a set of break rules based on the chart
_BREAK_RULES = _build_break_rules_set()


del _GCB_CHART, _GCB_VALUES


def EGC(unistr):
    """Splits the provided Unicode string into a list of its constituent
    extended grapheme clusters.

    Args:
        unistr (str): The Unicode string to split.

    Raises:
        TypeError: If `unistr` is not a string.
        ValueError: If `unistr` is an empty string.

    Returns:
        list: A list of strings, where each element represents an individual
            extended grapheme cluster.

    Examples:
        >>> EGC("e\u0301le\u0300ve")
        ['é', 'l', 'è', 'v', 'e']

        >>> egc = EGC("Z̷̳̎a̸̛ͅl̷̻̇g̵͉̉o͒")
        >>> for cluster in egc:
        ...     " ".join(f"{ord(char):04X}" for char in cluster)
        ...
        '005A 0337 030E 0333'
        '0061 0338 031B 0345'
        '006C 0337 0307 033B'
        '0067 0335 0309 0349'
        '006F 0352'

    """
    if not isinstance(unistr, str):
        raise TypeError(f"expected a string, but got {type(unistr).__name__}")

    if not unistr:
        raise ValueError("expected a non-empty string")

    elements = [*map(_PROP.get, map(ord, unistr))]

    if elements.count(None) == len(elements):
        return [*unistr]

    conjunct_linker_cluster_indices = set([
        match.end() for match in _RE_CONJUNCT_LINKER_CLUSTER.finditer(unistr)
    ])

    break_positions = [0]

    stack = []
    prev = None
    ep_index = None
    ri_count = 0

    for i, curr in enumerate(elements):
        if i == 0:
            pass

        elif i in conjunct_linker_cluster_indices and prev is not None:
            # https://www.unicode.org/reports/tr29/tr29-45.html#GB9c
            # Do not break within certain combinations
            # with Indic_Conjunct_Break (InCB)=Linker.
            pass

        elif curr == "Extended_Pictographic" and prev == "ZWJ":
            # https://www.unicode.org/reports/tr29/tr29-45.html#GB11
            # Do not break within emoji modifier sequences
            # or emoji zwj sequences.
            non_extend = not all(x in _EXTEND for x in stack[ep_index : i - 1])
            if ep_index is None or non_extend:
                break_positions.append(i)

        elif curr == "Regional_Indicator" and prev == "Regional_Indicator":
            # https://www.unicode.org/reports/tr29/tr29-45.html#GB12
            # https://www.unicode.org/reports/tr29/tr29-45.html#GB13
            # Do not break within emoji flag sequences. That is, do not break
            # between regional indicator (RI) symbols if there is an odd number
            # of RI characters before the break point.
            ri_count += 1
            if ri_count % 2 == 0:
                break_positions.append(i)

        elif (prev, curr) in _BREAK_RULES:
            break_positions.append(i)

        if curr == "Extended_Pictographic":
            ep_index = i

        stack.append(curr)
        prev = curr

    if len(break_positions) == 1:  # break_positions == [0]
        return [unistr]

    break_positions.append(len(unistr))

    return [unistr[i:j] for i, j in zip(break_positions, break_positions[1:])]


if __name__ == "__main__":
    import doctest
    doctest.testmod()
