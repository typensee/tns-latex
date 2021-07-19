#! /usr/bin/env python3

# ----------------- #
# -- DEV. "TEST" -- #
# ----------------- #

if __name__ == "__main__":
    from common import *

else:
    from .common import *


# ----------- #
# -- TOOLS -- #
# ----------- #

###
# prototype::
#     projpath = ; # See Python typing...
#                the path of the directory of the monorepo to explore.
#
#     return = ; # See Python typing...
#              the list of the ``PPath`` of the packages to build or update.
###

def packdirs(projpath: PPath) -> List[PPath]:
    packsfound: List[PPath] = []

    for subdir in projpath.walk("dir::"):
# A folder to analyze.
        if keepthisdir(subdir):
            packsfound.append(subdir)

# Sort the result and return it.
    packsfound.sort()

    return packsfound


###
# prototype::
#     dirpath = ; # See Python typing...
#               the path of the directory to analyze or not.
#
#     return = ; # See Python typing...
#              ``True`` for a directory to analyze, or 
#              ``False`` if the folder must be ignored.
###

def keepthisdir(dirpath: PPath) -> bool:
    if dirpath.name.startswith("x-") and dirpath.name.endswith("-x"):
        return False
    
# Looking for a ``about.peuf``.
    for aboutfile in dirpath.walk("file::about.peuf"):
        return keepthisabout(aboutfile)

# No ``about.peuf`` found.
    return False


###
# prototype::
#     aboutfile = ; # See Python typing...
#                 the path of an ``about.peuf`` file.
#
#     return = ; # See Python typing...
#              ``True`` if the ``about.peuf`` indicates a ¨tnslatex package, or 
#              ``False`` in other cases.
#
# warning::
#     Errors ares raised in if the path::``PEUF`` file is bad formatted.
###

def keepthisabout(aboutfile: PPath) -> bool:
    with ReadBlock(
        content = aboutfile,
        mode    = ABOUT_PEUF_MODE
    ) as datas:
        infos = datas.mydict("std nosep nonb")

    if GENE_TAG in infos:
        infos = infos[GENE_TAG]

        return (
            GENE_TNSLATEX_TAG in infos
            and
            infos[GENE_TNSLATEX_TAG] == YES_TAG
        )

    return False


# ----------------- #
# -- DEV. "TEST" -- #
# ----------------- #

if __name__ == "__main__":
    projectdir = PPath(__file__)

    while(not projectdir.name.startswith('typensee-latex')):
        projectdir = projectdir.parent

    for ppath in packdirs(projectdir):
        print(ppath)