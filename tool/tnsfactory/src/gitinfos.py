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
#     monorepopath = ; # See Python typing...
#                    the path of the directory of the monorepo to update.
#     allpacks     = ; # See Python typing...
#                    the list of the ``PPath`` of the ¨tnslatex packages.
#
#     return = ; # See Python typing...
#              the list of the ``PPath`` of the packages to build or update.
###

def packschanged(
    monorepopath: PPath,
    allpacks    : List[PPath]
) -> List[PPath]:
    with cd(monorepopath):
        gitoutput = runthis("git a")

    packstoupdate: List[PPath] = []

    for packpath in allpacks:
        packpath_str = str(packpath - monorepopath)
        
        if packpath_str in gitoutput:
            packstoupdate.append(packpath)

    return packstoupdate


# ----------------- #
# -- DEV. "TEST" -- #
# ----------------- #

if __name__ == "__main__":
    projectdir = PPath(__file__)

    while(not projectdir.name.startswith('typensee-latex')):
        projectdir = projectdir.parent

    allpacks = [
        projectdir / "tool/bdoc",
    ]

    for ppath in packschanged(projectdir, allpacks):
        print(ppath)