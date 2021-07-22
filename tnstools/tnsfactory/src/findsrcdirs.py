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

        methodused = f"TOC in ``{anadir.dir_relpath / ABOUT_NAME}``"

# No ``about.peuf`` with files or dirs to use.
    else:
        assert kind in TOC.ALL_PHYSICAL_KINDS, \
               f'kind = "{kind}" for srcdirs not in {TOC.ALL_PHYSICAL_KINDS}.'

        for fileordir in anadir.dirpath.walk(f"{kind}::*"):
# Something to analyze directly in our folder?
            relpath = fileordir - anadir.dirpath
            
            if (
                relpath.depth == 0 
                and
                keepthis(fileordir, kind)
            ):
                paths.append(fileordir)
                
        paths.sort()

        methodused = f"automatic walk in ``{anadir.dir_relpath}``"

# Some dirs found.
    if paths:
        plurial = "" if len(paths) == 1 else "s"
        
        anadir.stepprints[0](
            f"{MESSAGE_SRC}: {len(paths)} {kind}{plurial} from {methodused}."
        )

# Nothing more to do.
    return paths
