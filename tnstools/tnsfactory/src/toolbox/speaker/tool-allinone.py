#! /usr/bin/env python3

from mistool.os_use     import PPath
from mistool.string_use import between
from orpyste.data       import ReadBlock

from spk_interface import *


# -------------------------------- #
# -- ONLY TOOLS FOR THE SOURCES -- #
# -------------------------------- #

# Esay-to-update configuration.

THIS_FILE = PPath(__file__)
FILE_PY   = THIS_FILE.parent / THIS_FILE.name.replace('tool-', '')
FILE_PEUF = THIS_FILE.parent / 'tool-config' / FILE_PY.with_ext('peuf').name


# Let's contruct.

THIS_TAG = "RECIPES"

COMMENT_TAG       = f'{THIS_TAG} - AUTO CODE'
COMMENT_TAG_START = f'# -- {COMMENT_TAG} - START -- #'
COMMENT_TAG_END   = f'# -- {COMMENT_TAG} - END -- #'


SRC_ACTIONS        = []
SRC_ACTIONS_NO_ARG = []


with ReadBlock(
    content = FILE_PEUF,
    mode    = "verbatim"
) as datas:
    for kind, names in datas.mydict("std nosep nonb").items():
        for onename in names:
            if not onename:
                continue

            if kind == "var":
                suffix = f'{kind.upper()}_'
            else:
                suffix = ""

            varname = f'{suffix}{onename.upper()}'

            SRC_ACTIONS.append(f'{varname} = "{onename}"')

            if kind in ["no_arg", "no_arg_allowed"]:
                SRC_ACTIONS_NO_ARG.append(varname)


# Let's nuild the source code.

TAB = " "*4


SRC_ACTIONS = "\n".join(SRC_ACTIONS)

SRC_ACTIONS_NO_ARG = "\n".join(
    f'{TAB}{code},'
    for code in SRC_ACTIONS_NO_ARG
)


CODE = f'''
{SRC_ACTIONS}

ACTIONS_NO_ARG = [
{SRC_ACTIONS_NO_ARG}
]
'''


# Let's update the FILE_PY.

with FILE_PY.open(
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


with FILE_PY.open(
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
