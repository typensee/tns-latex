#!/usr/bin/env python3

from mistool.os_use import cd, runthis

from orpyste.data      import ReadBlock
from orpyste.parse.ast import ASTError

from ..base import *

from .config import *
from .toc import *
from ..problems import *


# -------------------------------- #
# -- GOOD FILES AND DIRECTORIES -- #
# -------------------------------- #

###
# This class proposes methods to search ¨tnslatex like packages or 
# ¨latex like sources to analyze.
###

class SearchDirFile(BaseCom):

###
# prototype::
#     monorepo    = ; // See Python typing...  
#                   the path of the directory of the monorepo.
#     speaker     = ; // See Python typing...  
#                   an instance of ``toolbox.speaker.allinone.Speaker`` 
#                   is used to communicate small ¨infos.
#     problems    = ; // See Python typing...  
#                   an instance of ``toolbox.Problems`` that manages 
#                   a basic history of the problems found.
###
    def __init__(
        self,
        monorepo: PPath,
        speaker : Speaker,
        problems: Problems,
    ) -> None:
        super().__init__(
            monorepo    = monorepo,
            speaker     = speaker ,
            problems    = problems,
        )

        self.about = None


###
# prototype::
#     onepath = ; // See Python typing...
#               a path of a file or a directory.
#     kind    = _ in [DIR_TAG, FILE_TAG]; // See Python typing...
#               the kind of infos wanted.
#
#     :return: = ; // See Python typing...
#                ``True`` for a file or a directory to keep and
#                ``False`` in the opposite case.
###
    def is_kept(
        self,
        onepath: PPath,
        kind   : str
    ) -> bool:
# Good kind?
        if kind == DIR_TAG:
            if not onepath.is_dir():
                return False

        else:
            if not onepath.is_file():
                return False

# Something to ignore?
        if any(
            not p.match(onepath.stem) is None
            for p in PATTERNS_SPECIAL[kind]
        ):
            return False

# Nothing more to do for folders.
        if kind == DIR_TAG:
            return True

# We keep only files with specific extensions.
        return onepath.ext in FILE_EXT_WANTED


###
# prototype::
#     onedir = ; // See Python typing...
#              the path of the directory to keep or not.
#
#     :return: = ; // See Python typing...
#                ``True`` for a directory whit  an ``about.peuf`` file, or 
#                ``False`` in other cases.
#
# This method manages the value of the attribut ``self.about``.
#
# warning::
#     If no about file is found, the value of ``self.about`` is ``None``.
###
    def has_about(self, onedir: PPath) -> bool:
        self.about = onedir / ABOUT_NAME

        if self.about.is_file():
            return True

        self.about = None

        return False

###
# prototype::
#     :return: = ; // See Python typing...
#                the "semantic dict" content of the ``about.peuf`` file.
#
# warning:
#     Use ``self.has_about`` before the call of this method.
###
    def about_content(self) -> dict:
        try:
            with ReadBlock(
                content = self.about,
                mode    = ABOUT_PEUF_MODE
            ) as datas:
                infos = datas.mydict("std nosep nonb")
    
        except ASTError:
            relpath = self.about - self.monorepo

            self.new_error(
                src_relpath = relpath,
                info        = f'about file "{relpath}" bad formatted.'
            )
            return 

        return infos
