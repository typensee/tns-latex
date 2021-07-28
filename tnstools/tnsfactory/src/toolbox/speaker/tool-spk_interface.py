#! /usr/bin/env python3

from mistool.os_use     import PPath
from mistool.string_use import between
from orpyste.data       import ReadBlock


# -------------------------------- #
# -- ONLY TOOLS FOR THE SOURCES -- #
# -------------------------------- #

# Esay-to-update configuration.

THIS_FILE = PPath(__file__)
FILE_PY   = THIS_FILE.parent / THIS_FILE.name.replace('tool-', '')
FILE_PEUF = THIS_FILE.parent / 'tool-config' / FILE_PY.with_ext('peuf').name


# Let's contruct.

THIS_TAG = "INTERFACE"

COMMENT_TAG       = f'{THIS_TAG} - AUTO CODE'
COMMENT_TAG_START = f'# -- {COMMENT_TAG} - START -- #'
COMMENT_TAG_END   = f'# -- {COMMENT_TAG} - END -- #'


CONTEXTS     = []           
ALL_CONTEXTS = []           


with ReadBlock(
    content = FILE_PEUF,
    mode    = "verbatim"
) as datas:
    for onename in datas.mydict("std nosep nonb")['ctxts']:
        if not onename:
            continue

        varname = f'CONTEXT_{onename.upper()}'

        CONTEXTS.append(f'{varname} = "{onename}"')
            
        ALL_CONTEXTS.append(varname)


# Let's nuild the source code.

TAB = " "*4

CONTEXTS = "\n".join(CONTEXTS)

ALL_CONTEXTS = f',\n{TAB}'.join(ALL_CONTEXTS)


CODE = f'''
{CONTEXTS}

ALL_CONTEXTS = [
{TAB}{ALL_CONTEXTS}
]
'''


# Let's update the file.

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
