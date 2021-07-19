#! /usr/bin/env python3

from typing import *

from mistool.os_use import cd, PPath, runthis
from mistool.string_use import between
from mistool.term_use import ALL_FRAMES, withframe

from orpyste.data import ReadBlock


# ----------------------- #
# -- CONSTANTS - ABOUT -- #
# ----------------------- #

TOC_TAG  = "toc"

GENE_TAG      = "general"
GENE_NEED_TAG = "need"
GENE_TNSLATEX_TAG = "tnslatex"

YES_TAG = "yes"
NO_TAG  = "no"


ABOUT_PEUF_MODE = {
    "keyval:: =": ":default:",
    "verbatim"  : TOC_TAG,
}


# ---------------------- #
# -- CONSTANTS - DECO -- #
# ---------------------- #

DECO = " "*4

LATEX_FRAME_1 = lambda t: withframe(
    text  = t,
    frame = ALL_FRAMES['latex_pretty_1']
)

LATEX_FRAME_2 = lambda t: withframe(
    text  = t,
    frame = ALL_FRAMES['latex_pretty_2']
)
