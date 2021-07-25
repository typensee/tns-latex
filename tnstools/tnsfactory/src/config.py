#! /usr/bin/env python3

from enum import Enum
import re

from mistool.os_use   import DIR_TAG, FILE_TAG
from mistool.term_use import ALL_FRAMES, withframe, Step


# ------------- #
# -- SOURCES -- #
# ------------- #

ABOUT_NAME   =  "about.peuf"
SRC_DIR_NAME =  "src"

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


MESSAGE_ERROR     = "ERROR"
MESSAGE_WARNING   = "WARNING"
MESSAGE_WRONG_SRC = "BAD SOURCE"


# ----------- #
# -- ABOUT -- #
# ----------- #

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


# -------------- #
# -- DECORATE -- #
# -------------- #

TAB_1 = " "*4
TAB_2 = TAB_1*2

NL  = lambda x = 0: print("" + "\n"*(x - 1))

for i in range(1, 3):
    exec(
    f"""
ASCII_FRAME_{i} = lambda t: withframe(
    text  = t,
    frame = ALL_FRAMES['pyba_title_{i}']
)
    """)


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


# -------------------- #
# -- TERMINAL TOOLS -- #
# -------------------- #

###
# This class colorize easily the terminal outputs.
###

# Source: GNU/Linux Mag. - Hors Série 115
class ColorTerm(Enum):
    normal :str = ''
    error  :str = '31'
    warning:str = '34'
    OK     :str = '36'

    def colorit(self) -> None:
        if self.value:
            termcode = f"\x1b[1;{self.value}m"

        else:
            termcode = f"\x1b[0m"

        print(termcode, end = "")


MAIN_STEPS = Step()

DECO_STEPS = [c for c in "*+"]

for i, deco in enumerate(DECO_STEPS, 1):
    exec(
    f"""
_SUB_{i}_STEPS = Step(
    textit = lambda n, t: TAB_{i} + f"{deco} {{t}}"
)

def SUB_{i}_STEPS(message):
    color_used = True

    if MESSAGE_ERROR in message:
        ColorTerm.error.colorit()
    
    elif MESSAGE_WARNING in message:
        ColorTerm.warning.colorit()
    
    elif "OK" in message:
        ColorTerm.OK.colorit()

    else:
        color_used = False

    _SUB_{i}_STEPS(message)

    if color_used:
        ColorTerm.normal.colorit()
    """)

