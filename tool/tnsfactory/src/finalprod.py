#! /usr/bin/env python3

from .common import *


# ----------- #
# -- TOOLS -- #
# ----------- #

###
# This class manages sources suchas to build the final product.
###

class FinalProd:
###
# prototype::
#     anadir = common.AnaDir ;  
#              any class having the ¨api of ``common.AnaDir``.
#     kind   = _ in TOC.ALL_USER_KINDS ; # See Python typing... 
#              the kind of ¨infos expected to be in the TOC.
###
    def __init__(
        self,
        anadir,# Can't use the type common.AnaDir (cyclic imports).
        kind: str
    ) -> None:
        self.anadir = anadir
        self.kind   = kind

        self.onefile = None

###
# prototype::
#     files = ; # See Python typing... 
#             the ???? .
###
    def addfiles(
        self,
        files: List[PPath]
    ) -> None:
        for self.onefile in files:
            if self.onefile.ext == STY_FILE_EXT:
                self.newSTY()

            else:
                self.newTEX()

            if not self.anadir.success:
                return

###
# ???? .
###
    def newTEX(self) -> None:
        print("TEX", self.onefile.name)

###
# ???? .
###
    def newSTY(self) -> None:
        print("STY", self.onefile.name)
