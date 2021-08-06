#!/usr/bin/env python3

from typing import *

import re

from mistool.os_use import PPath, DIR_TAG, FILE_TAG


# -------------------- #
# -- LANG SUPPORTED -- #
# -------------------- #

LANG_FR = "FR"
LANG_EN = "EN"

ALL_LANGS =[
    LANG_FR, 
    LANG_EN
]

LOCALE_DIR    = "locale"
TRANSLATE_DIR = "translate"

# TODO extension pour les fichiers LANG!!!

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
# -- IGNORE THIS DIR - AUTO CODE - START -- #
            "changes?",
            "configs?",
            "datas?",
            "tests?",
            "tools?",
# -- IGNORE THIS DIR - AUTO CODE - END -- #
        ]
    ],
    FILE_TAG: [
        re.compile(f"^{p}$")
        for p in PATTERN_COMMON + [
# -- IGNORE THIS FILE - AUTO CODE - START -- #
            "tests?-.*",
            "tools?-.*",
# -- IGNORE THIS FILE - AUTO CODE - END -- #
        ]
    ]
}


# --------------------------- #
# -- EXTENSIONS OF SOURCES -- #
# --------------------------- #

TEX_FILE_EXT = "tex"
STY_FILE_EXT = "sty"

FILE_EXT_WANTED = [ 
    STY_FILE_EXT,
    TEX_FILE_EXT,
]


PATTERN_LATEX_DOC_ALL_LANGS = '|'.join(ALL_LANGS)
PATTERN_LATEX_DOC           = re.compile(
    f"^.*-({PATTERN_LATEX_DOC_ALL_LANGS})$"
)
    


# --------------- #
# -- RESOURCES -- #
# --------------- #

EXTRA_RESOURCES = "RESOURCES"
