"""Unicode default extended grapheme clusters."""

from pyuegc.unicode import (
    _GCB_PROP_VAL,  # grapheme cluster break property values
    _EXT_PICTOGR,   # extended pictographic characters
)

_GCB_PROP_VAL.update(dict.fromkeys(_EXT_PICTOGR, "Extended_Pictographic"))

# Grapheme cluster break chart
# https://www.unicode.org/Public/15.0.0/ucd/auxiliary/GraphemeBreakTest.html
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
    None,       # used in lieu of "Other"
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

_EXT_VALUES = {
    "Extend",
    "Extended_Pictographic",
}


def _nobreak_rules():
    nobreak = []
    for i, sublist in enumerate(_GCB_CHART):
        for j, val in enumerate(sublist):
            if not val:
                nobreak.append((_GCB_VALUES[i], _GCB_VALUES[j]))
    return set(nobreak)


_NOBREAK = _nobreak_rules()


del _EXT_PICTOGR, _GCB_CHART, _GCB_VALUES


def EGC(unistr):
    """Split the original Unicode string *unistr* to a list
    of extended grapheme clusters.
    """
    values = [_GCB_PROP_VAL.get(ord(u)) for u in unistr]

    if values == [None] * len(values):
        return [*unistr] if unistr else []

    # Grapheme breakpoints
    breakpoints = []
    stack = []
    prev = ext_pict_idx = None
    ri_count = 0
    for i, curr in enumerate(values):
        if not i:
            breakpoints.append(1)
        else:
            if prev == "Extended_Pictographic":
                ext_pict_idx = i - 1
            if curr == "Extended_Pictographic" and prev == "ZWJ":
                # https://www.unicode.org/reports/tr29/tr29-41.html#GB11
                # Do not break within emoji modifier sequences
                # or emoji zwj sequences.
                if ext_pict_idx is None:
                    breakpoints.append(1)
                else:
                    tmp = [
                        1 if x in _EXT_VALUES else 0
                        for x in stack[ext_pict_idx : i - 1]
                    ]
                    breakpoints.append(0 if tmp and all(tmp) else 1)
            elif curr == "Regional_Indicator" and prev == "Regional_Indicator":
                # https://www.unicode.org/reports/tr29/tr29-41.html#GB12
                # https://www.unicode.org/reports/tr29/tr29-41.html#GB13
                # Do not break within emoji flag sequences. That is, do not
                # break between regional indicator (RI) symbols if there is
                # an odd number of RI characters before the break point.
                ri_count += 1
                breakpoints.append(0 if ri_count & 1 else 1)
            else:
                breakpoints.append(0 if (prev, curr) in _NOBREAK else 1)

        prev = curr
        stack.append(prev)

    breakpoints.append(1)

    # Grapheme clusters
    egc = []
    prev = 0
    for i, j in enumerate(breakpoints):
        if j and i:
            egc.append(unistr[prev:i])
            prev = i

    return egc
