#! /usr/bin/env python3

from collections import defaultdict

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

        self.onefile        = None
        self.onefile_lines  = None
        self.onefile_blocks = None
        self.secblock       = None


###
# prototype::
#     files = ; # See Python typing... 
#             a list of source files.
###
    def anafiles(
        self,
        files: List[PPath]
    ) -> None:
        for self.onefile in files:
            self.ana_onefile()

            if not self.anadir.success:
                continue

            # if self.onefile.ext == STY_FILE_EXT:
            #     self.newSTY()

            # elif self.onefile.ext == TEX_FILE_EXT:
            #     self.newTEX()

            # else:
            #     raise NotImplementedError(
            #         f'missing extension "{self.onefile.ext}".'
            #     )

            if not self.anadir.success:
                return


###
# Working on a TEX file.
###
    def newTEX(self) -> None:
        TEX






###
# Working on a STY file.
###
    def newSTY(self) -> None:
        STY





###
# Preparing the analysis of one file.
###
    def ana_onefile(self) -> None:
        self.communicate()
        self.build_filelines()
        self.find_blocks()

        from pprint import pprint;pprint(self.onefile_blocks)

###
# Let's talk to the world...
###
    def communicate(self) -> None:
        message = (
            f'{MESSAGE_WORKING_ON} the {self.onefile.ext.upper()} '
            f'file "{self.onefile.name}".'
        )
        
        self.anadir.loginfo(
            message = message,
            isitem  = True
        )

###
# The lines of the file to analyze.
###
    def build_filelines(self) -> None:
        with open(
            file     = self.onefile,
            encoding = "utf-8",
            mode     = "r"
        ) as onefile:
            self.onefile_lines = onefile.read().splitlines()

###
# This method find all structural blocks useful for the final product.
###
    def find_blocks(self) -> None:
        self.secblock       = FILE_BLOCK[self.onefile.ext]
        self.onefile_blocks = defaultdict(list)

        lastsection: str = ""

        for oneline in self.onefile_lines:
            kindofline = self.kindof(oneline)

# A new block open.
            if kindofline:
                lastsection = kindofline

                if lastsection in self.onefile_blocks:
                    self.anadir.success = False
                    
                    message = f'"{lastsection}" can\'t be used more than one time.'

                    self.anadir.error(message)
                    self.anadir.stepprints[0](f"{MESSAGE_ERROR}: {message}")

                    return                

# Just one line excpet before the first block.
            elif lastsection:
                self.onefile_blocks[lastsection].append(oneline)



###
# prototype::
#     oneline = ; # See Python typing... 
#               one line of source file.
#
#     return = ; # See Python typing... 
#              a spectial title in comments or an empty string.
#
# This method find the kind of the line.
###
    def kindof(
        self,
        oneline: str
    ) -> str:
        oneline = oneline.strip()

        if oneline in self.secblock:
# Remove ``% ==`` and ``== %``
            if "==" in oneline:
                oneline = oneline.split("==")
                oneline = oneline[1].strip()

# Human version of a LaTeX command.
            else:
                for last, new in [
                    ("\\", ""),
                    ("{" , "-"),
                    ("}" , ""),
                ]:
                    oneline = oneline.replace(last, new)
                
                oneline = oneline.upper()

            return oneline

        return ""