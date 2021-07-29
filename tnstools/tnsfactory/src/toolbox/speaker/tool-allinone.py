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


ACTION_TAG = 'action'
VAR_TAG    = 'var'

SRC_ACTIONS_OR_VARS = {
    ACTION_TAG: [],
    VAR_TAG   : [],
}

SRC_MAXLEN_ACTIONS_OR_VARS = {
    ACTION_TAG: 0,
    VAR_TAG   : 0,
}

SRC_ACTIONS_NO_ARG = []


with ReadBlock(
    content = FILE_PEUF,
    mode    = "verbatim"
) as datas: 
    config = {}
    
    for kind, names in datas.mydict("std nosep nonb").items():
        config[kind] = []

        for onename in names:
            if not onename:
                continue

            config[kind].append(onename)

            if kind == VAR_TAG:
                thistype =  VAR_TAG
            
            else:
                thistype = ACTION_TAG
            
            lenname = len(onename)
            
            if lenname > SRC_MAXLEN_ACTIONS_OR_VARS[thistype]:
                SRC_MAXLEN_ACTIONS_OR_VARS[thistype] = lenname


for kind, names in config.items():
    for onename in names:
        if kind == VAR_TAG:
            thistype = kind
            suffix   = f'{kind.upper()}_'

        else:
            thistype = ACTION_TAG
            suffix   = ""

        varname = f'{suffix}{onename.upper()}'
        spaces  = " "*(SRC_MAXLEN_ACTIONS_OR_VARS[thistype] - len(onename))

        SRC_ACTIONS_OR_VARS[thistype].append(f'{varname}{spaces} = "{onename}"')

        if kind in ["no_arg", "no_arg_allowed"]:
            SRC_ACTIONS_NO_ARG.append(varname)


# Let's nuild the source code.

TAB = " "*4


for key, vals in SRC_ACTIONS_OR_VARS.items():
    SRC_ACTIONS_OR_VARS[key] = "\n".join(sorted(vals))

SRC_ACTIONS_NO_ARG = "\n".join(
    f'{TAB}{code},'
    for code in sorted(SRC_ACTIONS_NO_ARG)
)


CODE = f'''
{SRC_ACTIONS_OR_VARS[ACTION_TAG]}

ACTIONS_NO_ARG = [
{SRC_ACTIONS_NO_ARG}
]

{SRC_ACTIONS_OR_VARS[VAR_TAG]}
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
