#! /usr/bin/env python3

from ..base import *

from .config import *


# ----------------------------------------- #
# -- LOOK FOR A TOC INSIDE AN ABOUT FILE -- #
# ----------------------------------------- #

###
# This class extracts ¨infos from a toc inside an ``about.peuf`` file 
# of a onedir.
###

class TOC(BaseCom):
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
#     monorepo = ; // See Python typing...  
#                the path of the directory of the monorepo.
#     onedir   = ; // See Python typing...
#                the p
#     level    = _ in [0..3] (0); // See Python typing...
#                the level of step indicating where ``0`` is for automatic 
#                numbered enumerations.ath of one onedir to analyze.
#     problems = ; // See Python typing...
#                an instance of ``toolbox.Problems`` that manages 
#                a basic history of the problems found.
#     infos    = _ in self.ALL_USER_KINDS ; // See Python typing... 
#                a dict returned by the method 
#                ``search.SearchDirFile.about_content``.
#     kind     = _ in self.ALL_USER_KINDS ; // See Python typing... 
#                the kind of ¨infos expected to be in the TOC.
###
    def __init__(
        self,
        monorepo: PPath,
        onedir  : PPath,
        problems: Problems,
        infos   : dict,
        kind    : str,
        level   : int
    ) -> None:
        super().__init__(
            monorepo = monorepo,
            problems = problems,
        )

        self.onedir = onedir
        
        self.infos = infos
        self.kind  = kind
       
        self.level = level


###
# prototype::
#     :return: = ; // See Python typing...
#                ``True`` if a key ``toc`` exits and ``False`` otherwise.
###
    def has_toc(self) -> bool:
        return TOC_TAG in self.infos

###
# prototype::
#     :return: = ; // See Python typing...
#                the list of "string" paths of the sources to analyze.
#
# info::
#     We know that the TOC block exists (this has been treated before using 
#     this method).
###
    def extract(self) -> List[str]:
# TOC block exists.
        pathsfound: List[str] = []

        for nbline, oneinfo in enumerate(
            self.infos[TOC_TAG],
            1
        ):
            kindfound, path = self.kindof(oneinfo)

            if kindfound == self.KIND_EMPTY:
                continue

# Bad TOC: wrong kind for an ¨io object.
            if self.kind != kindfound:
                message = "problem with the about file. "
                
                if kindfound in self.ALL_USER_KINDS:
                    message += f'Only {self.kind}s allowed.'

                else:
                    message += f'Illegal line.'

                message += (
                    "\n" 
                    f"See the line {nbline} (rel. nb) with the following content:"
                    "\n" 
                    f'" {oneinfo} "'
                )

                self.new_error(
                    src_relpath = self.onedir - self.monorepo,
                    info        = message,
                    level       = self.level
                )

                return

# Complete short names for STY files.
            if (
                self.kind == self.KIND_FILE 
                and
                not '.' in path
            ):
                path = f'{path}.{STY_FILE_EXT}'

# A new path found.
            pathsfound.append(path)

# Empty TOC.
        if not pathsfound:
            self.new_error(
                src_relpath = self.onedir - self.monorepo,
                info        = 'about file: empty TOC!',
                level       = self.level
            )

            return

# Everything seems ok.
        return pathsfound


###
# prototype::
#     :return: = ; // See Python typing...
#                ``[kind, info]`` where ``kind`` belongs to ``self.ALL_KINDS`` and 
#                info can be ``None`` in case of problem, or the text after
#                the placeholder.
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
