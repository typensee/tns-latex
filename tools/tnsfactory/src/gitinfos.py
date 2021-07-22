#! /usr/bin/env python3

from .common import *


# ----------- #
# -- TOOLS -- #
# ----------- #

###
# prototype::
#     monorepo = ; # See Python typing...
#                the path of the directory of the monorepo to update.
#     allpacks = ; # See Python typing...
#                the list of the ``PPath`` of the ¨tnslatex packages.
#
#     return = ; # See Python typing...
#              the list of the ``PPath`` of the packages to build or update.
###

def packschanged(
    monorepo: PPath,
    allpacks: List[PPath]
) -> List[PPath]:
    with cd(monorepo):
        gitoutput = runthis("git a")

    packstoupdate: List[PPath] = []

    for packpath in allpacks:
        packpath_str = str(packpath - monorepo)
        
        if packpath_str in gitoutput:
            packstoupdate.append(packpath)

    return packstoupdate
