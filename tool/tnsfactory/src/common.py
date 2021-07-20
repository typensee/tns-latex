#! /usr/bin/env python3

from typing import *

from mistool.os_use import cd, PPath, runthis
from mistool.string_use import between
from mistool.term_use import ALL_FRAMES, withframe, Step

from orpyste.data import ReadBlock, PeufError

from .logit import *


# ------------ #
# -- CODING -- #
# ------------ #

ABOUT_NAME     =  "about.peuf"
SRC_DIR_NAME   =  "src"
PROTECTED_DIRS = ["changes"]


# -------------- #
# -- MESSAGES -- #
# -------------- #

ABOUT_MESSAGE = f"``{ABOUT_NAME}`` file > "


# ----------- #
# -- ABOUT -- #
# ----------- #

TOC_TAG  = "toc"
GENE_TAG = "general"

ABOUT_PEUF_MODE = {
    "keyval:: =": ":default:",
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

DECO = " "*4

ASCII_FRAME = lambda t: print(
    withframe(
        text  = t,
        frame = ALL_FRAMES['ascii_star']
    )
)

LATEX_FRAME_1 = lambda t: print(
    withframe(
        text  = t,
        frame = ALL_FRAMES['latex_pretty_1']
    )
)

LATEX_FRAME_2 = lambda t: print(
    withframe(
        text  = t,
        frame = ALL_FRAMES['latex_pretty_2']
    )
)

NL = lambda x = 0: print("" + "\n"*(x - 1))


# ------------- #
# -- CLASSES -- #
# ------------- #

###
# This class is used by classes working on directories.
###

class AnaDir:
###
# prototype::
#     monorepo  = ; # See Python typing...
#                      the path of the directory of the monorepo to explore.
#     dirpath   = ; # See Python typing...
#                      the path of one package to build or update.
#     stepprint = ; # See Python typing...
#                 the function used to print ¨infos in the terminal.
#     logfile   = ; # See Python typing...
#                 the path of the log file.
#     needabout = ; # See Python typing...
#                 ``True`` allows that ``about.peuf`` is missing,
#                 contrary to ``False``.
###
    def __init__(
        self,
        monorepo : PPath,
        dirpath  : PPath,
        stepprint: Callable[[str], None],
        logfile  : PPath,
        needabout: bool = False
    ) -> None:
        self.monorepo  = monorepo
        self.dirpath   = dirpath
        self.stepprint = stepprint
        self.logfile   = logfile
        self.needabout = needabout

        self.dir_relpath = dirpath - monorepo
        self.logger      = Logger(self)

###
# prototype::
#     message = ; # See Python typing...
#               the error message to append to the log file.
###
    def error(
        self,
        message: str
    ) -> None:
        self.logger.error(message)
        self.success = False

###
# prototype::
#     message = ; # See Python typing...
#               the warning message to append to the log file.
###
    def warning(
        self,
        message: str
    ) -> None:
        self.logger.warning(message)
