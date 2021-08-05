#! /usr/bin/env python3

from collections import defaultdict

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

START_TAG = "START"
END_TAG   = "END"

COMMENTS = defaultdict(dict)

for kind in ["sty", "tex"]:
    COMMENT_TAG = f'{kind.upper()} SPECIAL SECTIONS - AUTO CODE'

    COMMENTS[kind][START_TAG] = f'# -- {COMMENT_TAG} - START -- #'
    COMMENTS[kind][END_TAG]   = f'# -- {COMMENT_TAG} - END -- #'


SPE_SECT = defaultdict(list)

SRC_SPACING = {}

with ReadBlock(
    content = FILE_PEUF,
    mode    = "verbatim"
) as datas: 
    config = {}
    
    for tag, names in datas.mydict("std nosep nonb").items():
        SRC_SPACING[tag] = 0

        for onename in names:
            if not onename:
                continue

            SPE_SECT[tag].append(onename.upper())

            size = len(onename)

            if size > SRC_SPACING[tag]:
                SRC_SPACING[tag] = size


# Let's update the FILE_PY.

TAB = '\n' + " "*4

VAR_DEFS  = defaultdict(list)
VAR_NAMES = defaultdict(list)

for tag, names in SPE_SECT.items():
    maxsize = SRC_SPACING[tag]

    for onename in names:
        spaces = " "*(maxsize - len(onename))

        varname = f'{tag.upper()}ION_{onename}'

        kind = tag.replace("_sect", "")

        VAR_NAMES[kind].append(f'{varname},')
        VAR_DEFS[kind] .append(f'{varname}{spaces} = "{onename}"')

VAR_NAMES["tex"].append("TEX_BEGIN_DOC")


CODES = {}

for kind in VAR_DEFS:
    CODES[kind]  = '\n'.join(VAR_DEFS[kind])
    CODES[kind] += f"""

{kind.upper()}_ALL_SECTIONS = [
    {TAB.join(VAR_NAMES[kind])}
]
""".rstrip()

with FILE_PY.open(
    encoding = "utf-8",
    mode     = "r"
) as file:
    content = file.read()


for kind, code in CODES.items():
    before, _ , after = between(
        text = content, 
        seps = [
            COMMENTS[kind][START_TAG],
            COMMENTS[kind][END_TAG]
        ],
        keepseps = True
    )

    content = f'{before}\n{code}\n{after}'


with FILE_PY.open(
    encoding = "utf-8",
    mode     = "w"
) as file:
    file.write(content)
