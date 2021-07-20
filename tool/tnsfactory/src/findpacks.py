#! /usr/bin/env python3

from .common import *


# ----------- #
# -- TOOLS -- #
# ----------- #

###
# prototype::
#     monorepo = ; # See Python typing...
#                the path of the directory of the monorepo to explore.
#
#     return = ; # See Python typing...
#              the list of the ``PPath`` of the ¨tnslatex packages.
###

def packdirs(monorepo: PPath) -> List[PPath]:
    packsfound: List[PPath] = []

    for subdir in monorepo.walk("dir::"):
# A folder to analyze.
        if keepthisdir(subdir):
            packsfound.append(subdir)

# Sort the result and return it.
    packsfound.sort()

    return packsfound


###
# prototype::
#     dirpath = ; # See Python typing...
#               the path of the directory to keep or not.
#
#     return = ; # See Python typing...
#              ``True`` for a directory to keep for analysis, or 
#              ``False`` if the folder must be ignored.
###

def keepthisdir(dirpath: PPath) -> bool:
    if ignorepath(dirpath):
        return False
    
# Looking for an ``about.peuf`` file.
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
#     Errors ares raised if the path::``PEUF`` file is bad formatted.
###

def keepthisabout(aboutfile: PPath) -> bool:
    with ReadBlock(
        content = aboutfile,
        mode    = ABOUT_PEUF_MODE
    ) as datas:
        infos = datas.mydict("std nosep nonb")

    if GENE_TAG in infos:
        infos = infos[GENE_TAG]

        return infos.get(GENE_TNSLATEX_TAG, None) == YES_TAG

    return False
