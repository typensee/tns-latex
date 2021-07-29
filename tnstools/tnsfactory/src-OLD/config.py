#! /usr/bin/env python3


import re

from mistool.os_use   import DIR_TAG, FILE_TAG



# ------------- #
# -- SOURCES -- #
# ------------- #


# -------------- #
# -- MESSAGES -- #
# -------------- #

LOG_ID, TERM_ID = range(2)

MESSAGE_WORKING = "Working"

MESSAGE_TEMPLATE_FILE = lambda name: f"``{name}`` file -> "

MESSAGE_ABOUT      = MESSAGE_TEMPLATE_FILE(ABOUT_NAME)
MESSAGE_SRC_ABOUT  = MESSAGE_TEMPLATE_FILE(f"{SRC_DIR_NAME}/{ABOUT_NAME}")
MESSAGE_SRC        = "Source"
MESSAGE_FINAL_PROD = "Final Product"

MESSAGE_WRONG_SRC = "BAD SOURCE"


# ----------- #
# -- ABOUT -- #
# ----------- #


# -------------- #
# -- DECORATE -- #
# -------------- #



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


# Z! Sorting must be respected.
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

EXTRA_RESOURCES = "RESOURCES"


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


