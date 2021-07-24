#! /usr/bin/env python3

from .common import *


# ----------- #
# -- TOOLS -- #
# ----------- #

###
# This class manages sources suchas to build the final product.
###

class FinalProd:
    XXX = "XXX"

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

        self.packpath           = None
        self.onefile            = None
        self.onefile_relpath    = None
        self.onefile_nb_n_lines = None
        self.onefile_blocks     = None

        self.final_blocks = {
            ext: {
                t: None
                for t in titles
                if t != TEX_END_DOC
            }
            for ext, titles in FILE_BLOCK.items()
        }


###
# prototype::
#     files = ; # See Python typing... 
#             a list of source files.
###
    def anafiles(
        self,
        packpath: PPath,
        files   : List[PPath]
    ) -> None:
        self.packpath = packpath

        for self.onefile in files:
            self.ana_onefile()

            if not self.anadir.success:
                continue

            # if self.onefile.ext == STY_FILE_EXT:
            #     self.newSTY()

            if self.onefile.ext == TEX_FILE_EXT:
                self.newTEX()

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
        if not TEX_BEGIN_DOC in self.onefile_blocks:
            VIDE
        
        print(self.onefile_relpath)
        print(self.onefile_blocks[TEX_BEGIN_DOC])

        # \subsection{:tech-sign:} <--- TEX_TECH_DYNA_SECTION






###
# Working on a STY file.
###
    def newSTY(self) -> None:
        STY






###
# Preparing the analysis of one file.
###
    def ana_onefile(self) -> None:
        self.onefile_relpath = self.onefile - self.packpath

        self.communicate()
        self.build_filelines()
        self.find_blocks()
        self.strip_blocks()


###
# The lines of the file to analyze.
###
    def build_filelines(self) -> None:
        with open(
            file     = self.onefile,
            encoding = "utf-8",
            mode     = "r"
        ) as onefile:
            self.onefile_nb_n_lines  = [
                (nbline, oneline.rstrip())
                for nbline, oneline in enumerate(onefile, start = 1)
            ]


###
# This method find all structural blocks useful for the final product.
###
    def find_blocks(self) -> None:
        self.secblock       = FILE_BLOCK[self.onefile.ext]
        self.onefile_blocks = defaultdict(list)

        lastsection: str = ""

        for nbline, oneline in self.onefile_nb_n_lines :
            kindofline = self.kindof(oneline)

# A new block open.
            if kindofline:
                message = ""

                if kindofline in self.onefile_blocks:
                    kindofline = self._comment_section(kindofline)
                    
                    message = f'"{kindofline}" can\'t be used more than one time.'

# The section must respect a sorting!
                elif (
                    lastsection
                    and
                    self.secblock.index(kindofline) <= self.secblock.index(lastsection)
                ):
                    kindofline = self._comment_section(kindofline)
                    
                    message = f'"% == {kindofline} == %" can\'t be after "{lastsection}".'

# Something wrong has been detected.
                if message:
                    self.anadir.success = False

                    message += (
                        f' Go to the line nb {nbline} in the file '
                        f'"{self.onefile.name}".'
                    )

                    self.anadir.problems.new_error(
                        src_relpath = self.onefile - self.anadir.monorepo,
                        message     = f'{message}',
                        level_term  = 2
                    )

                    return

                lastsection = kindofline

# Just one line excpet before the first block.
            elif lastsection:
                self.onefile_blocks[lastsection].append(
                    (nbline, oneline)
                )

# We do not need TEX_END_DOC key (it is here just to simplify the coding).
        if TEX_END_DOC in self.onefile_blocks:
            del self.onefile_blocks[TEX_END_DOC]

###
# prototype::
#     kind = ; # See Python typing... 
#            short version of special section in comment.
#
#     return = ; # See Python typing... 
#              long version of special section in comment.
###
    def _comment_section(self, kind: str) -> str:
        return f'% == {kind} == %'

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

# Remove ``% ==`` and ``== %``
        if "==" in oneline:
            oneline = oneline.split("==")

            if len(oneline) != 3:
                return ""

            oneline = oneline[1].strip()

        if oneline in self.secblock:
            return oneline

        return ""


###
# This method removes initial and final lines.
#
# warning::
#     We can't act on other empty lines because of the use of verbatim 
#     or listing environment for example.
###
    def strip_blocks(self) -> None:
        for section, content in self.onefile_blocks.items():
            while(content[0][1] == ''):
                content.pop(0)

            while(content[-1][1] == ''):
                content.pop(-1)

###
# Let's talk to the world...
###
    def communicate(self) -> None:
        message = (
            f'{MESSAGE_WORKING_ON} the {self.onefile.ext.upper()} '
            f'file "{self.onefile.name}".'
        )
        
        self.anadir.terminfo(
            message = message,
            level   = 1
        )
        
        self.anadir.loginfo(
            message = message,
            isitem  = True
        )