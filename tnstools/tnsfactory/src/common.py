#! /usr/bin/env python3

from typing import *

from collections import defaultdict
from enum import Enum
import re

from mistool.os_use import PPath, cd, runthis, DIR_TAG, FILE_TAG
from mistool.string_use import between
from mistool.term_use import ALL_FRAMES, withframe, Step

from orpyste.data import ReadBlock, PeufError

from .logit import *


# ------------ #
# -- CODING -- #
# ------------ #

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

TEX_FILE_EXT    = "tex"
STY_FILE_EXT    = "sty"
FILE_EXT_WANTED = [TEX_FILE_EXT, STY_FILE_EXT]


COM_SECT_PACKAGE = "PACKAGE"
COM_SECT_OPTIONS = "OPTIONS"
COM_SECT_TOOLS   = "TOOLS"

COM_SECT_EXTRAS = "EXTRAS"

TEX_BEGIN_DOC =  "\\begin{document}"
TEX_END_DOC   =  "\\end{document}"

TEX_TECH_DYNA_SECTION = ":tech-sign:"

# Z! Sorting must be respected.
FILE_BLOCK = {
# Special blocks for TEX files.
    STY_FILE_EXT: [
        title
        for title in [
            COM_SECT_PACKAGE,
            COM_SECT_OPTIONS,
            COM_SECT_TOOLS,
        ]
    ],
# Special blocks for TEX files.
    TEX_FILE_EXT: [
        title
        for title in [
            COM_SECT_EXTRAS,
        ]
    ] + [
        TEX_BEGIN_DOC,
        TEX_END_DOC,
    ], 
}


# -------------- #
# -- MESSAGES -- #
# -------------- #

LOG_ID, TERM_ID = range(2)

MESSAGE_TEMPLATE_FILE = lambda name: f"``{name}`` file -> "

MESSAGE_ABOUT      = MESSAGE_TEMPLATE_FILE(ABOUT_NAME)
MESSAGE_SRC_ABOUT  = MESSAGE_TEMPLATE_FILE(f"{SRC_DIR_NAME}/{ABOUT_NAME}")
MESSAGE_SRC        = "Source"
MESSAGE_FINAL_PROD = "Final Product"

MESSAGE_ERROR     = "ERROR"
MESSAGE_WARNING   = "WARNING"
MESSAGE_WRONG_SRC = "BAD SOURCE"

MESSAGE_WORKING_ON = "Working on"


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


# ----------- #
# -- TOOLS -- #
# ----------- #

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


###
# prototype::
#     onepath = ; # See Python typing...
#               a path of a file or a directory.
#     kind    = _ in [DIR_TAG, FILE_TAG]; # See Python typing...
#               the kind of infos wanted.
#
#     return  = ; # See Python typing...
#               ``True`` for a file or a directory to keep and
#               ``False`` in the opposite case.
###

def keepthis(
    onepath: PPath,
    kind   : bool
) -> bool:
# Something to ignore?
    if any(
        not p.match(onepath.stem) is None
        for p in PATTERNS_SPECIAL[kind]
    ):
        return False

# Nothing more to do for folders.
    if kind == DIR_TAG:
        return True

# We keep only files with specific extensions.
    return onepath.ext in FILE_EXT_WANTED


###
# This class is used by classes analyzing directories.
###

class AnaDir:
###
# prototype::
#     monorepo   = ; # See Python typing...
#                  the path of the directory of the monorepo to explore.
#     dirpath    = ; # See Python typing...
#                  the path of one package to build or update.
#     stepprints = ; # See Python typing...
#                  the functions used to print ¨infos in the terminal.
#     logfile    = ; # See Python typing...
#                  the path of the log file.
#     needabout  = ; # See Python typing...
#                  ``True`` allows that ``about.peuf`` is missing,
#                  contrary to ``False``.
###
    def __init__(
        self,
        monorepo  : PPath,
        dirpath   : PPath,
        stepprints: List[Callable[[str], None]],
        logfile   : PPath,
        needabout : bool = False
    ) -> None:
        self.monorepo   = monorepo
        self.dirpath    = dirpath
        self.stepprints = stepprints
        self.logfile    = logfile
        self.needabout  = needabout

        self.dir_relpath = dirpath - monorepo
        self.logger      = Logger(logfile)


###
# prototype::
#     context    = _ in [MESSAGE_ERROR, MESSAGE_WARNING]; # See Python typing...
#                  the kind of problem.
#     message    = ; # See Python typing...
#                  the error message to append to the log file.
#     pb_nb      = ; # See Python typing...
#                  the number of the problem.
#     level_term = (1) ; # See Python typing...
#                  the numer of tbabulation to use.
###
    def new_pb(
        self,
        context   : str,
        message   : str,
        pb_nb     : int,
        level_term: int = 1
    ) -> None:
        self.stepprints[level_term - 1](f'{context}: {message}.')

        self.logger.newpb(
            context = context,
            pb_nb   = pb_nb,
            message = message
        )


###
# A newline in the log file.
###
    def logNL(self):
        self.logger.NL()

###
# prototype::
#     message = ; # See Python typing...
#               the message to append to the log file.
#     isitem  = ; # See Python typing...
#               ``True`` indicates to print an item and
#               ``False`` to no do that. 
#     isnewdir = ; # See Python typing...
#                ``True`` when starting to work on an new
#                folder and ``False`` in other cases.
#     level    = (0); # See Python typing...
#                the level of indentation.
###
    def loginfo(
        self,
        message : str,
        isitem  : bool = False,
        isnewdir: bool = False,
        level   : int  = 0
    ) -> None:
        if isitem:
            message = self.logger.itemize(
                message = message,
                level   = level
            )

            if isnewdir:
                self.logNL()

        else:
            self.logNL()

        self.logger.appendthis(message)
        self.logNL()

###
# prototype::
#     message = ; # See Python typing...
#               the error message to print in the terminal.
#     level   = ; # See Python typing...
#               the level of indentation.
###
    def terminfo(
        self,
        message: str,
        level  : int = 0
    ) -> None:
        self.stepprints[level](message)
