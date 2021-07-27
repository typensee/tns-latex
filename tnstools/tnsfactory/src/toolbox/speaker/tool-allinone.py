#! /usr/bin/env python3

from mistool.os_use     import PPath
from mistool.string_use import between
from orpyste.data       import ReadBlock

from spk_interface import *


# -------------------------------- #
# -- ONLY TOOLS FOR THE SOURCES -- #
# -------------------------------- #

# Esay-to-update configuration.

FILE = PPath(__file__)
FILE = FILE.parent / FILE.name.replace('tool-', '')

CONFIG = """
no_arg::
    forlog
    forterm
    forall

no_arg_allowed::
    NL
    style

arg::
    print
    title
    step
    problem

var::
    step_info
    title
    level
    context
    info
    pb_id
"""


# Let's contruct.

THIS_TAG = "RECIPES"

COMMENT_TAG       = f'{THIS_TAG} - AUTO CODE'
COMMENT_TAG_START = f'# -- {COMMENT_TAG} - START -- #'
COMMENT_TAG_END   = f'# -- {COMMENT_TAG} - END -- #'


SRC_ACTIONS        = []
SRC_ACTIONS_NO_ARG = []

SRC_STYLES = []          


with ReadBlock(
    content = CONFIG,
    mode    = "verbatim"
) as datas:
    for kind, names in datas.mydict("std nosep nonb").items():
        for onename in names:
            if kind == "var":
                suffix = f'_{kind.upper()}'
            else:
                suffix = ""

            varname = f'SPK{suffix}_{onename.upper()}'

            SRC_ACTIONS.append(f'{varname} = "{onename}"')

            if kind in ["no_arg", "no_arg_allowed"]:
                SRC_ACTIONS_NO_ARG.append(varname)


for ctxt in ALL_CONTEXTS:
    varname   = f'SPK_STYLE_{ctxt.upper()}'
    valuename = f'CONTEXT_{ctxt.upper()}'
    
    SRC_STYLES.append(f'{varname} = {valuename}')


# Let's nuild the source code.

TAB = " "*4


SRC_ACTIONS = "\n".join(SRC_ACTIONS)

SRC_ACTIONS_NO_ARG = "\n".join(
    f'{TAB}{code},'
    for code in SRC_ACTIONS_NO_ARG
)


SRC_STYLES = "\n".join(SRC_STYLES)


CODE = f'''
{SRC_ACTIONS}

SPK_ACTIONS_NO_ARG = [
{SRC_ACTIONS_NO_ARG}
]


{SRC_STYLES}

SPK_ALL_STYLES = ALL_CONTEXTS
'''


# Let's update the file.

with FILE.open(
    encoding = "utf-8",
    mode     = "r"
) as file:
    content = file.read()


before, _ , after = between(
    text = content, 
    seps = [
        COMMENT_TAG_START,
        COMMENT_TAG_END
    ],
    keepseps = True
)


with FILE.open(
    encoding = "utf-8",
    mode     = "w"
) as file:
    file.write(
        f'''
{before}
{CODE}
{after}
        '''.strip()+ "\n"
    )
