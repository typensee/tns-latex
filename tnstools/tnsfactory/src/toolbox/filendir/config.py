#!/usr/bin/env python3

from typing import *

import re

from mistool.os_use import PPath, DIR_TAG, FILE_TAG


# ----------- #
# -- ABOUT -- #
# ----------- #

ABOUT_NAME   =  "about.peuf"
SRC_DIR_NAME =  "src"

TOC_TAG  = "toc"
GENE_TAG = "general"

ABOUT_PEUF_MODE = {
    "keyval:: =": GENE_TAG,
    "verbatim"  : TOC_TAG,
}

GENE_TNSLATEX_TAG = "tnslatex"
GENE_DESC_TAG     = "desc"
GENE_AUTHOR_TAG   = "author"
GENE_LICENCE_TAG  = "licence"
GENE_NEED_TAG     = "need"

GENE_ALL_TAGS = set([
    GENE_TNSLATEX_TAG,
    GENE_DESC_TAG    ,
    GENE_AUTHOR_TAG  ,
    GENE_LICENCE_TAG ,
    GENE_NEED_TAG    ,
])

YES_TAG = "yes"
NO_TAG  = "no"


# ------------ #
# -- IGNORE -- #
# ------------ #

PATTERN_COMMON = [
    "\\..+",
    "x-.+-x",
]

PATTERNS_SPECIAL = {
    DIR_TAG: [
        re.compile(f"^{p}$")
        for p in PATTERN_COMMON + [
            "changes", 
            "tools", 
            "tests"
        ]
    ],
    FILE_TAG: [
        re.compile(f"^{p}$")
        for p in PATTERN_COMMON + [
            "tools?-.*", 
            "tests?-.*"
        ]
    ]
}


# --------------- #
# -- RESOURCES -- #
# --------------- #

EXTRA_RESOURCES = "RESOURCES"


# --------------------- #
# -- TEX/STY SOURCES -- #
# --------------------- #

TEX_FILE_EXT    = "tex"
STY_FILE_EXT    = "sty"
FILE_EXT_WANTED = [TEX_FILE_EXT, STY_FILE_EXT]


STY_SECT_PACKAGE = "PACKAGE"
STY_SECT_OPTIONS = "OPTIONS"
STY_SECT_TOOLS   = "TOOLS"

STY_SECTIONS = [
    STY_SECT_PACKAGE,
    STY_SECT_OPTIONS,
    STY_SECT_TOOLS,
]


TEX_SECT_EXTRAS = "EXTRAS"
TEX_BEGIN_DOC   =  "\\begin{document}"
TEX_END_DOC     =  "\\end{document}" # Just here to simplify 
                                     # the implementation.

TEX_SECTIONS = [
    TEX_SECT_EXTRAS,
    TEX_BEGIN_DOC,
]


# -------
# WARNING
# -------
# 
# Sorting must be respected.
FILE_BLOCK = {
# Special blocks for TEX files.
    STY_FILE_EXT: [
        title
        for title in STY_SECTIONS
    ],
# Special blocks for TEX files.
    TEX_FILE_EXT: [
        title
        for title in TEX_SECTIONS + [TEX_END_DOC]
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
\emph
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
