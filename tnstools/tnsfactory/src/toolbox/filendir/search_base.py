#!/usr/bin/env python3

from orpyste.data      import ReadBlock
from orpyste.parse.ast import ASTError

from ..base import *

from .config import *
from .toc import *
from ..problems import *


# ----------------------------------------------- #
# -- BASE CLASS FOR GOOD FILES AND DIRECTORIES -- #
# ----------------------------------------------- #

###
# This class proposes methods to search ¨tnslatex like packages and 
# files to analyze.
###

class SearchDirFile(BaseCom):

###
# prototype::
#     monorepo = ; // See Python typing...  
#                the path of the directory of the monorepo.
#     problems = ; // See Python typing...  
#                an instance of ``toolbox.Problems`` that manages 
#                a basic history of the problems found.
###
    def __init__(
        self,
        monorepo: PPath,
        problems: Problems,
    ) -> None:
        super().__init__(
            monorepo = monorepo,
            problems = problems,
        )

        self.last_about = None


###
# prototype::
#     onedir      = ; // See Python typing...  
#                   the path of a directory .
#     kind        = _ in [DIR_TAG, FILE_TAG]; // See Python typing...
#                   the kind of ¨io objects wanted.
#     main_reldir = ; // See Python typing...
#                   a path of a containing directory.
#
#     :return: = ; // See Python typing...
#                this method iterates unrecursively inside the content of
#                a directory and yields the ¨io object found that are not
#                ignored regarding the specifications of the ¨tnslatex 
#                like packages.
#
#     :see: = self.is_kept
###
    def iterIO(
        self, 
        onedir     : PPath, 
        kind       : str,
        main_reldir: PPath,
    ) -> Iterator[PPath]:
        for fileordir in onedir.iterdir():
            if self.is_kept(
                onepath     = fileordir,
                kind        = kind,
                main_reldir = main_reldir
            ):
                yield fileordir

###
# prototype::
#     onepath     = ; // See Python typing...
#                   a path of a file or a directory.
#     kind        = _ in [DIR_TAG, FILE_TAG]; // See Python typing...
#                   the kind of infos wanted.
#     main_reldir = ; // See Python typing...
#                   a path of a containing directory.
#
#     :return: = ; // See Python typing...
#                ``True`` for a file or a directory to keep and
#                ``False`` in the opposite case.
###
    def is_kept(
        self,
        onepath    : PPath,
        kind       : str,
        main_reldir: PPath,
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
        if not onepath.ext in FILE_EXT_WANTED:
            return False

# ¨latex doc must be name like ``mydioc-EN.tex``.
        if onepath.ext == TEX_FILE_EXT:
            if PATTERN_LATEX_DOC.match(onepath.stem) is None:
                self.new_warning(
                    src_relpath = main_reldir,
                    info        = (
                        f'LaTeX file ignored "{onepath.name}". '
                        f'Use a name like "{onepath.name}-EN.{TEX_FILE_EXT}".'
                    ),
                    level = 2
                )

                return False
        

# No more things to teste for a file.
        return True


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
        self.last_about = onedir / ABOUT_NAME

        if self.last_about.is_file():
            return True

        self.last_about = None

        return False

###
# prototype::
#     level = _ in [0..3] (0); // See Python typing...
#             the level of step indicating where ``0`` is for automatic 
#             numbered enumerations (this for emitting errors).
#
#     :return: = ; // See Python typing...
#                the "semantic dict" content of the ``about.peuf`` file.
#
# warning:
#     ``self.has_about``  **must be used just before** the call of 
#     this method.
###
    def about_content(self, level: int = 0) -> dict:
        try:
            with ReadBlock(
                content = self.last_about,
                mode    = ABOUT_PEUF_MODE
            ) as datas:
                infos = datas.mydict("std nosep nonb")
    
        except ASTError:
            relpath = self.last_about - self.monorepo

            self.new_error(
                src_relpath = relpath,
                info        = f'about file "{relpath}" bad formatted.',
                level       = level
            )
            return 

        return infos
