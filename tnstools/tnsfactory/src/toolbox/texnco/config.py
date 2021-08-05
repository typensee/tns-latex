#!/usr/bin/env python3

from typing import *

from ..filendir import TEX_FILE_EXT, STY_FILE_EXT


# -------------------- #
# -- TEX/STY CODING -- #
# -------------------- #

# The order used is important !

# -- STY SPECIAL SECTIONS - AUTO CODE - START -- #
STY_SECTION_PACKAGES = "PACKAGES"
STY_SECTION_OPTIONS  = "OPTIONS"
STY_SECTION_TOOLS    = "TOOLS"

STY_ALL_SECTIONS = [
    STY_SECTION_PACKAGES,
    STY_SECTION_OPTIONS,
    STY_SECTION_TOOLS,
]
# -- STY SPECIAL SECTIONS - AUTO CODE - END -- #


TEX_BEGIN_DOC = "\\begin{document}"
TEX_END_DOC   = "\\end{document}" # Just here to simplify 
                                  # the implementation.

# -- TEX SPECIAL SECTIONS - AUTO CODE - START -- #
TEX_SECTION_EXTRAS = "EXTRAS"

TEX_ALL_SECTIONS = [
    TEX_SECTION_EXTRAS,
    TEX_BEGIN_DOC
]
# -- TEX SPECIAL SECTIONS - AUTO CODE - END -- #


# -------
# WARNING
# -------
# 
# Sorting must be respected.
FILE_BLOCK = {
# Special blocks for TEX files.
    STY_FILE_EXT: [
        title
        for title in STY_ALL_SECTIONS
    ],
# Special blocks for TEX files.
    TEX_FILE_EXT: [
        title
        for title in TEX_ALL_SECTIONS + [TEX_END_DOC]
    ], 
}


# --------------- #
# -- LATEX DOC -- #
# --------------- #

LATEX_SECTIONS = [
    section
    for section in r"""
\section
\subsection
\subsubsection
\paragraph
:NOT-USED-AFTER:
    """.strip().split("\n")
]

LATEX_LOWER_SECTIONS = {
    section: LATEX_SECTIONS[len(LATEX_SECTIONS) - i]
    for i, section in enumerate(LATEX_SECTIONS[::-1][1:], 1)
}

LATEX_SECTIONS.pop(-1)

NB_LATEX_SECTIONS = len(LATEX_SECTIONS)

LATEX_SECTIONS_INDEXES = {
    section: i
    for i, section in enumerate(LATEX_SECTIONS)
}


LATEX_TECH_SIGN_TITLE = ":techsign:"

LATEX_TECH_SECTIONS = {
    f'{section}{{{LATEX_TECH_SIGN_TITLE}}}': section
    for section in LATEX_SECTIONS
}
