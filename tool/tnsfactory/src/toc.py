#! /usr/bin/env python3

from .common import *


# ----------- #
# -- TOOLS -- #
# ----------- #

###
# This class extracts ¨infos from a toc form a ``about.peuf`` of a package.
###

class TOC:
    ITEM_DIR : str = "+"
    ITEM_FILE: str = "*"
    ITEM_PACK: str = ">"

    KIND_DIR  : str = "DIR"
    KIND_FILE : str = "FILE"
    KIND_PACK : str = "PACK"
    KIND_PB   : str = "illegal"
    KIND_EMPTY: str = "empty"

    ALL_USER_KINDS = [
        KIND_DIR,
        KIND_FILE,
        KIND_PACK,
    ]

###
# prototype::
#     anadir     = common.AnaDir ;  
#                  a class with the ¨api contains in ``common.AnaDir``.
#     kindwanted = ; # See Python typing... 
#                  the kind of ¨infos expected to be in the TOC.
###
    def __init__(
        self,
        anadir,# Can't use the type common.AnaDir (cyclic imports).
        kindwanted: str
    ) -> None:
        self.anadir     = anadir
        self.kindwanted = kindwanted

###
# prototype::
#     return = ; # See Python typing...
#              the list of directories to analyze.
###
    def build(self) -> List[PPath]:
        assert(self.kindwanted in self.ALL_USER_KINDS)

        pathsfound: List[PPath] = []

        for nbline, oneinfo in enumerate(
            self.anadir.about[TOC_TAG],
            1
        ):
            kindfound, path = self.kindof(oneinfo)

            if kindfound == self.KIND_EMPTY:
                continue

            if self.kindwanted != kindfound:
                message = ABOUT_MESSAGE
                
                if kindfound in self.ALL_USER_KINDS:
                    message += f"only {self.kindwanted}S allowed. "

                else:
                    message += f"illegal line. "

                message += (
                    f"See the line {nbline} (rel. nb): "
                    f"...|{oneinfo}|..."
                )

                self.anadir.error(message)
                return

            pathsfound.append(path)

# Evmpty TOC.
        if not pathsfound:
            self.anadir.error("``about.peuf`` file: empty TOC!")
            return

# Everything seems ok.
        return pathsfound

###
# prototype::
#     return = ; # See Python typing...
#              the list of directories to analyze.
###
    def kindof(self, oneinfo: str):# -> List[str, str]:
        oneinfo = oneinfo.strip()

        if not oneinfo:
            return self.KIND_EMPTY, None
        
        if len(oneinfo) == 1:
            return self.KIND_PB, None

        firstchar, otherchars = oneinfo[0], oneinfo[1:].lstrip()

        for kind in self.ALL_USER_KINDS:
            if firstchar == getattr(self, f"ITEM_{kind}"):
                return getattr(self, f"KIND_{kind}"), otherchars
            
        return self.KIND_PB, None
