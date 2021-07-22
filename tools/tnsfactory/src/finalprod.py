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
###
    def __init__(
        self,
        anadir,# Can't use the type common.AnaDir (cyclic imports).
    ) -> None:
        self.anadir = anadir

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
# Working on a TEX file.
###
    def newTEX(self) -> None:
        print("TEX", self.onefile.name)

###
# Working on a STY file.
###
    def newSTY(self) -> None:
        print("STY", self.onefile.name)
