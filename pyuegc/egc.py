"""Unicode default extended grapheme clusters."""

import re

from pyuegc.unicode import (
    _GCB_PROP,  # grapheme cluster break property values
    _EXT_PICT,  # extended pictographic characters
    _LINKING_CONSONANTS,
    _CONJUNCT_LINKERS,
    _EXT_CCC_ZWJ,
)

_PROP = {**_GCB_PROP, **dict.fromkeys(_EXT_PICT, "Extended_Pictographic")}

# Regex pattern object used to match certain
# conjunct linker clusters (Indic aksaras)
_re_conjunct_linker_cluster = re.compile(
    f"    [ {_LINKING_CONSONANTS} ]  "              # LinkingConsonant
    f"    [ {_EXT_CCC_ZWJ}        ]* "              # ExtCccZwj*
    f"    [ {_CONJUNCT_LINKERS}   ]  "              # ConjunctLinker
    f"    [ {_EXT_CCC_ZWJ}        ]* "              # ExtCccZwj*
    f" (?=[ {_LINKING_CONSONANTS} ]) ", re.VERBOSE  # LinkingConsonant
)

del _GCB_PROP, _EXT_PICT, _LINKING_CONSONANTS, _CONJUNCT_LINKERS, _EXT_CCC_ZWJ

# Grapheme cluster break chart
# https://www.unicode.org/Public/15.1.0/ucd/auxiliary/GraphemeBreakTest.html
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


_BREAK_RULES = _build_break_rules_set()


del _GCB_CHART, _GCB_VALUES


def EGC(unistr):
    """Split the original Unicode string *unistr* into a list
    of extended grapheme clusters.
    """
    elems = [_PROP.get(ord(u)) for u in unistr]

    if elems.count(None) == len(elems):
        return [*unistr]

    conj_linker_cluster_i = set()

    for match in _re_conjunct_linker_cluster.finditer(unistr):
        i, j = match.span()
        conj_linker_cluster_i.update(range(i + 1, j + 1))

    positions = [0]

    stack = []
    prev = extpict_i = None
    ri_count = 0
    for i, curr in enumerate(elems):
        if i == 0:
            pass
        elif i in conj_linker_cluster_i:
            # https://www.unicode.org/reports/tr29/tr29-43.html#GB9c
            # Do not break within certain combinations with ConjunctLinker.
            # assert stack[-1] is None
            continue
        elif curr == "Extended_Pictographic" and prev == "ZWJ":
            # https://www.unicode.org/reports/tr29/tr29-43.html#GB11
            # Do not break within emoji modifier sequences
            # or emoji zwj sequences.
            if extpict_i is None \
                    or not all(x in _EXTEND for x in stack[extpict_i : i - 1]):
                positions.append(i)
        elif curr == "Regional_Indicator" and prev == "Regional_Indicator":
            # https://www.unicode.org/reports/tr29/tr29-43.html#GB12
            # https://www.unicode.org/reports/tr29/tr29-43.html#GB13
            # Do not break within emoji flag sequences. That is, do not
            # break between regional indicator (RI) symbols if there is
            # an odd number of RI characters before the break point.
            ri_count += 1
            if not ri_count % 2:
                positions.append(i)
        elif (prev, curr) in _BREAK_RULES:
            positions.append(i)

        if curr == "Extended_Pictographic":
            extpict_i = i

        prev = curr
        stack.append(prev)

    positions.append(i + 1)  # i + 1 == len(unistr)

    if len(positions) == 2:  # [0, len(unistr)]
        return [unistr]

    return [unistr[i:j] for i, j in zip(positions, positions[1:])]
