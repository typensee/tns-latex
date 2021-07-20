#! /usr/bin/env python3

from .about  import *
from .common import *
from .toc    import *


# ----------- #
# -- TOOLS -- #
# ----------- #

###
# prototype::
#     anadir     = common.AnaDir ;  
#                  a class with the ¨api contains in ``common.AnaDir``.
#     kindwanted = ; # See Python typing... 
#                  the kind of ¨infos expected to be in the TOC.
#
#     return = ; # See Python typing...
#              the list of the ``PPath`` of the sources of a package.
###

def srcdirs(
    anadir,# Can't use the type common.AnaDir (cyclic imports).
    kindwanted: str
) -> List[PPath]:
# Let's be optimism.
    anadir.success = True

    subdirs:List[PPath] = []

    about_src = About(anadir).build()

# ``about.peuf`` found but some problems found.
    if not anadir.success:
        return

# Good ``about.peuf``.
    elif not anadir.about is None:
        subdirs = TOC(
            anadir     = anadir,
            kindwanted = kindwanted
        ).build()

        if not anadir.success:
            return

        methodused = "TOC in the ``src`` folder"

# No ``about.peuf``.
    else:
        for onesubdir in anadir.dirpath.walk("dir::"):
# A folder to analyze.
            relpath = onesubdir - anadir.dirpath
            
            if (
                relpath.depth == 0
                and
                not relpath.name in PROTECTED_DIRS
            ):
                subdirs.append(onesubdir)
                
        subdirs.sort()

        methodused = "automatic walk in the ``src`` folder"

# No dir found!
    if not subdirs:
        anadir.error("No source found.")
        anadir.success = False
        return

# Some dirs found.
    plurial = "" if len(subdirs) == 1 else "s"
    anadir.stepprint(
        f"{len(subdirs)} source dir{plurial} found (method used: {methodused})"
    )

    return subdirs