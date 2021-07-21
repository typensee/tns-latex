#! /usr/bin/env python3

from .about  import *
from .common import *
from .toc    import *


# ----------- #
# -- TOOLS -- #
# ----------- #

###
# prototype::
#     anadir = common.AnaDir ;  
#              any class having the ¨api of ``common.AnaDir``.
#     kind   = ; # See Python typing... 
#              the kind of ¨infos expected to be in the TOC.
#
#     return = ; # See Python typing...
#              the list of the ``PPath`` of the sources wanted.
###

def srcdirs(
    anadir,# Can't use the type common.AnaDir (cyclic imports).
    kind: str
) -> List[PPath]:
# Let's be optimism.
    anadir.success = True

    paths:List[PPath] = []

    about_src = About(anadir).build()

# ``about.peuf`` found but with some problems.
    if not anadir.success:
        return

# Good ``about.peuf``.
    elif not anadir.about is None:
        paths = TOC(
            anadir = anadir,
            kind   = kind
        ).build()

        if not anadir.success:
            return

        methodused = f"TOC in ``{SRC_DIR_NAME}/{ABOUT_NAME}``"

# No ``about.peuf`` with files or dirs to search.
    else:
        assert kind in TOC.ALL_PHYSICAL_KINDS, \
               f'kind = "{kind}" for srcdirs not in {TOC.ALL_PHYSICAL_KINDS}.'

        for onesubdir in anadir.dirpath.walk(f"{kind}::*"):
# Directly in our folder?
            relpath = onesubdir - anadir.dirpath
            
            if relpath.depth != 0:
                continue

# Something to ignore?
            if ignorepath(onesubdir):
                continue

# A folder to analyze.
            if kind == TOC.KIND_DIR:
                if not relpath.name in PROTECTED_DIRS:
                    paths.append(onesubdir)

            else:
                paths.append(onesubdir)
                
        paths.sort()

        methodused = f"automatic walk in ``{SRC_DIR_NAME}``"

# No dir found!
    if not paths:
        anadir.warning("no source found.")
        return paths

# Some dirs found.
    plurial = "" if len(paths) == 1 else "s"
    
    anadir.stepprints[0](
        MESSAGE_SRC + f"{len(paths)} {kind}{plurial} from {methodused}."
    )

    return paths
