#! /usr/bin/env python3

from .common import *


# ----------- #
# -- TOOLS -- #
# ----------- #

###
# This class analyses TEX sources.
###

class BuildTEX:
###
# prototype::
#     finalprod = finalprod.FinalProd ;  
#                 any class having the ¨api of ``inalprod.FinalProd``.
###
    def __init__(
        self,
        finalprod,# Can't use the type inalprod.FinalProd (cyclic imports).
    ) -> None:
        self.anadir = finalprod.anadir

        self.ext = TEX_FILE_EXT
        
        self.file_relpath = finalprod.onefile_relpath 
        self.blocks       = finalprod.onefile_blocks

        self.final_blocks = {
            kind: []
            for kind in TEX_SECTIONS + [LATEX_TECH_SIGN_TITLE]
        }
        
        self.secfound = ["" for _ in range(len(LATEX_SECTIONS))]

        self.nbline  = None
        self.oneline = None

###
# Here is the great bandleader.
###
    def build(self):
# Let's go!
        for methodname in [
            "build_extras",
            "build_doc",
            "minicontent",
        ]:
            getattr(self, methodname)()

            if not self.anadir.success:
                return


###
# This method....
###
    def build_extras(self):
        if not TEX_SECT_EXTRAS in self.blocks:
            return

# We just have to keep the content of the lines without their number.
        self.final_blocks[TEX_SECT_EXTRAS] = [
            line
            for _, line in self.blocks[TEX_SECT_EXTRAS]
        ]

###
# This method....
###
    def build_doc(self):
        if not TEX_BEGIN_DOC in self.blocks:
            return

        is_normal_content = True

        posmax = len(self.blocks[TEX_BEGIN_DOC]) - 1
        pos    = -1

        while(pos < posmax):
            pos += 1
            
            self.nbline, self.oneline = self.blocks[TEX_BEGIN_DOC][pos]

            kind = self.kindof(self.oneline.strip())

# Nothing special to do.
            if kind in LATEX_TECH_SECTIONS:
                title = self.validate_techsecfound(kind)

                if not self.anadir.success:
                    return

                is_normal_content = False
                self.final_blocks[LATEX_TECH_SIGN_TITLE].append(title)

# A "normal" section
            elif kind in LATEX_SECTIONS:
# We can have to add one to the position to take care 
# of titles on two lines.
                pos, title = self.validate_secfound(pos, posmax)

                if not self.anadir.success:
                    return
                
# Title seems "basically" okay.
                self.update_secfound(kind)

                is_normal_content = True
                self.final_blocks[TEX_BEGIN_DOC].append(title)

            
# Add this line to the human doc.
            elif is_normal_content:
                self.final_blocks[TEX_BEGIN_DOC].append(self.oneline)

# Add this line to the tech doc.
            else:
                self.final_blocks[LATEX_TECH_SIGN_TITLE].append(self.oneline)

###
# ???
###
    def minicontent(self):
        for kind, content in self.final_blocks.items():
            for i in (-1, 0):
                while(content and content[i] == ''):
                    content.pop(i)
            
            if kind != TEX_SECT_EXTRAS and not content:
                if kind == TEX_BEGIN_DOC:
                    message = "no human doc found"
                
                else:
                    message = "no technical doc found"
                
                self.anadir.problems.new_warning(
                    src_relpath = self.file_relpath,
                    message     = message
                )


###
# prototype::
#     linestriped = ; // See Python typing... 
#                   ???
#
#     return = ; // See Python typing...
#              ???
###
    def kindof(self, linestriped: str) -> str:
# A technical section?
#
# We do this first because sections are found by just looking 
# for lines starting with a LaTeX section...
        for techsec in LATEX_TECH_SECTIONS:
            if techsec == linestriped:
                return techsec

# A "normal" section
        for sec in LATEX_SECTIONS:
            if linestriped.startswith(sec):
                return sec

# TODO: An import?  
# TODO: An image?

# Nothing
        return ""



###
# ???
###
    def validate_techsecfound(
        self,
        kind: str
    ) -> str:
        secid = LATEX_SECTIONS.index(
            LATEX_TECH_SECTIONS[kind]
        )

        title = self.secfound[secid]

# No corresponding title...
        if not title:
            self.anadir.success = False
            
            self.anadir.problems.new_error(
                src_relpath = self.file_relpath,
                message     = (
                     'no corresponding section for a technical one. '
                    f'See line {self.nbline}.'
                )
            )

# A corresponding title: we a have to update the list of last section found
# and to keep the info that a tech section is treated.

        return title

###
# ???
###
    def validate_secfound(
        self,
        pos    : int, 
        posmax : int
    ) -> int:
# We must take car of a possible title written on two lines like 
# in the following example.
#
#   \section{\texorpdfstring{Title with $\partial$}%
#                           {Title with "rounded d"}}
        title   = self.oneline
        message = ""

        if not self.goodbalanced(title):
            if pos == posmax:
                message = self._error_message_unbalanced(self.nbline)
                    
            else:
                title += "\n" + self.blocks[TEX_BEGIN_DOC][pos + 1][1]
                
                if not self.goodbalanced(title): 
                    message = self._error_message_unbalanced(self.nbline)

# One problem found.
        if message:
            self.anadir.success = False
            
            self.anadir.problems.new_error(
                src_relpath = self.file_relpath,
                message     = message
            )

# Next position.
        return pos, title


###
# prototype::
#     newkind = ; // See Python typing... 
#               ???
#     oneline = ; // See Python typing... 
#               ???
#
# This method....
###
    def update_secfound(
        self, 
        newkind: str
    ) -> None:
        index = LATEX_SECTIONS_INDEXES[newkind]

# Lower sections must be "removed".
        for i in range(index+1, NB_LATEX_SECTIONS):
            self.secfound[i] = ""

# Update the actual section found.
        self.secfound[index] = self.oneline


###
# prototype::
#     return = ; // See Python typing... 
#              ???
#
# This method....
###
    def goodbalanced(self, content: str) -> bool:
        if not "{" in content:
            return False

        nbbraces = 0

        for c in content:
            if c == '{':
                nbbraces += 1

            elif c == '}':
                nbbraces -= 1

                if nbbraces < 0:
                    return False
        
        if nbbraces != 0:
            return False

        return True

##
    def _error_message_unbalanced(self, nbline: int) -> str:
        return  f'unbalanced braces for a section. See line {nbline}'