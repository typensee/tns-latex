#! /usr/bin/env python3

from .common import *
from mistool.os_use import DIR_TAG, FILE_TAG

# ----------- #
# -- TOOLS -- #
# ----------- #

###
# This class extracts ¨infos from a toc inside an ``about.peuf`` 
# file of a package.
###

class TOC:
    ITEM_DIR : str = "+"
    ITEM_FILE: str = "*"
    ITEM_PACK: str = ">"

    KIND_DIR  : str = DIR_TAG
    KIND_FILE : str = FILE_TAG
    KIND_PACK : str = "pack"
    KIND_PB   : str = "illegal"
    KIND_EMPTY: str = "empty"

    ALL_PHYSICAL_KINDS: List[str] = [
        KIND_DIR,
        KIND_FILE
    ]

    ALL_USER_KINDS: List[str] = ALL_PHYSICAL_KINDS + [
        KIND_PACK,
    ]

    ALL_KINDS: List[str] = ALL_USER_KINDS + [
        KIND_PB,
        KIND_EMPTY,
    ]

###
# prototype::
#     anadir = common.AnaDir ;  
#              any class having the ¨api of ``common.AnaDir``.
#     kind   = _ self.LL_USER_KINDS ; # See Python typing... 
#              the kind of ¨infos expected to be in the TOC.
###
    def __init__(
        self,
        anadir,# Can't use the type common.AnaDir (cyclic imports).
        kind: str
    ) -> None:
        assert kind in self.ALL_USER_KINDS, \
               f'kind = "{kind}" for TOC not in {self.ALL_USER_KINDS}.'

        self.anadir = anadir
        self.kind   = kind

###
# prototype::
#     return = ; # See Python typing...
#              the list of directories to analyze.
###
    def build(self) -> List[PPath]:
# No TOC block!
        if not TOC_TAG in self.anadir.about:
            self.anadir.error(f"``{ABOUT_NAME}`` file: no TOC block!")
            return

# TOC block exists.
        assert(self.kind in self.ALL_USER_KINDS)

        pathsfound: List[PPath] = []

        for nbline, oneinfo in enumerate(
            self.anadir.about[TOC_TAG],
            1
        ):
            kindfound, path = self.kindof(oneinfo)

            if kindfound == self.KIND_EMPTY:
                continue

            if self.kind != kindfound:
                message = MESSAGE_SRC_ABOUT
                
                if kindfound in self.ALL_USER_KINDS:
                    message += f"only {self.kind}S allowed. "

                else:
                    message += f"illegal line. "

                message += (
                    "\n" 
                    f"See the line {nbline} (rel. nb) with the following content:"
                    "\n" 
                    f"-->|{oneinfo}|<--"
                )

                self.anadir.error(message)
                return

            pathsfound.append(path)

# Empty TOC.
        if not pathsfound:
            self.anadir.error(f"``{ABOUT_NAME}`` file: empty TOC!")
            return

# Everything seems ok.
        return pathsfound

###
# prototype::
#     return = ; # See Python typing...
#              ``[kind, info]`` where ``kind`` belongs to ``self.ALL_KINDS`` and 
#              info can be ``None`` in case of problem, or the text after
#              the placeholder.
###
    def kindof(self, oneinfo: str):# -> List[str, str]:
        oneinfo = oneinfo.strip()

        if not oneinfo:
            return self.KIND_EMPTY, None
        
        if len(oneinfo) == 1:
            return self.KIND_PB, None

        firstchar, otherchars = oneinfo[0], oneinfo[1:].lstrip()

        for kind in self.ALL_USER_KINDS:
            kind = kind.upper()

            if firstchar == getattr(self, f"ITEM_{kind}"):
                return getattr(self, f"KIND_{kind}"), otherchars
            
        return self.KIND_PB, None
