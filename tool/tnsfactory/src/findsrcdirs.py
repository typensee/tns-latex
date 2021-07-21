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
#                  any class having the ¨api of ``common.AnaDir``.
#     kindwanted = ; # See Python typing... 
#                  the kind of ¨infos expected to be in the TOC.
#
#     return = ; # See Python typing...
#              the list of the ``PPath`` of the sources wanted.
###

def srcdirs(
    anadir,# Can't use the type common.AnaDir (cyclic imports).
    kindwanted: str
) -> List[PPath]:
# Let's be optimism.
    anadir.success = True

    subdirs:List[PPath] = []

    about_src = About(anadir).build()

# ``about.peuf`` found but with some problems.
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

        methodused = f"TOC in ``{SRC_DIR_NAME}/{ABOUT_NAME}``"

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
                if not ignorepath(onesubdir):
                    subdirs.append(onesubdir)
                
        subdirs.sort()

        methodused = f"automatic walk in ``{SRC_DIR_NAME}``"

# No dir found!
    if not subdirs:
        anadir.error("no source found.")
        anadir.success = False
        return subdirs

# Some dirs found.
    plurial = "" if len(subdirs) == 1 else "s"
    
    anadir.stepprints[0](
        MESSAGE_SRC + f"{len(subdirs)} dir{plurial} from {methodused}."
    )

    return subdirs
