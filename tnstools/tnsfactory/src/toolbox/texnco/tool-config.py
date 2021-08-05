#! /usr/bin/env python3

from collections import defaultdict

from mistool.os_use     import DIR_TAG, FILE_TAG, PPath
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

ALL_IO_TAGS = [DIR_TAG, FILE_TAG]

START_TAG = "START"
END_TAG   = "END"

COMMENTS = defaultdict(dict)

for tag in ALL_IO_TAGS:
    COMMENT_TAG = f'IGNORE THIS {tag.upper()} - AUTO CODE'

    COMMENTS[tag][START_TAG] = f'# -- {COMMENT_TAG} - START -- #'
    COMMENTS[tag][END_TAG]   = f'# -- {COMMENT_TAG} - END -- #'


IO_PATTERNS_IGNORED = defaultdict(list)

TEMPLATE_PATTERNS = {
    FILE_TAG: '"{onename}s?-.*",',
    DIR_TAG : '"{onename}s?",',
}

with ReadBlock(
    content = FILE_PEUF,
    mode    = "verbatim"
) as datas: 
    config = {}
    
    for kind, names in datas.mydict("std nosep nonb").items():
        kind = kind.replace("ignore-", "")

        if kind == "all":
            tags = ALL_IO_TAGS
        
        elif kind == FILE_TAG:
            tags = [FILE_TAG]

        elif kind == DIR_TAG:
            tags = [DIR_TAG]

        else:
            BUG

        for onename in names:
            if not onename:
                continue

            for onetag in tags:
                IO_PATTERNS_IGNORED[onetag].append(
                    TEMPLATE_PATTERNS[onetag].format(onename = onename)
                )


# Let's update the FILE_PY.

TAB = " "*4*3

IO_PATTERNS_IGNORED = {
    tag: sorted(names)
    for tag, names in IO_PATTERNS_IGNORED.items()
}

IO_PATTERNS_IGNORED = {
    tag: TAB + f'\n{TAB}'.join(names)
    for tag, names in IO_PATTERNS_IGNORED.items()
}


with FILE_PY.open(
    encoding = "utf-8",
    mode     = "r"
) as file:
    content = file.read()


for tag, code in IO_PATTERNS_IGNORED.items():
    before, _ , after = between(
        text = content, 
        seps = [
            COMMENTS[tag][START_TAG],
            COMMENTS[tag][END_TAG]
        ],
        keepseps = True
    )

    content = f'{before}\n{code}\n{after}'


with FILE_PY.open(
    encoding = "utf-8",
    mode     = "w"
) as file:
    file.write(content)
