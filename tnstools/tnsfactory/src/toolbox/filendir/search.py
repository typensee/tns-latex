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

        self.packs_paths = []


###
# This methods builds the sorted list of the ``PPath`` of the ¨tnslatex  
# packages to analyze.
###
    def buildpaths(self) -> None:
        self.packs_paths = self.rec_buildpaths(self.monorepo)
        self.packs_paths.sort()

###
# prototype::
#     onedir = ; // See Python typing...
#              the path of a directory to explore.
#
#     :return: = ; // See Python typing...
#                the **unsorted** list of the ``PPath`` of the ¨tnslatex 
#                like packages to analyze.
###
    def rec_buildpaths(self, onedir: PPath) -> List[PPath]:
        packsfound: List[PPath] = []

        for subdir in onedir.iterdir():
# A folder to analyze.
            if (
                subdir.is_dir() 
                and 
                self.is_not_ignored(subdir, DIR_TAG)
            ):
                if self.is_tnspack(subdir):
                    packsfound.append(subdir)

                else:
                    packsfound += self.rec_buildpaths(subdir)

        return packsfound


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
    def is_not_ignored(
        self,
        onepath: PPath,
        kind   : str
    ) -> bool:
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
#                ``True`` for a directory which is a ¨tnslatex like one, or 
#                ``False`` in other cases.
###
    def is_tnspack(self, onedir: PPath) -> bool:
        aboutpath = onedir / ABOUT_NAME

        return aboutpath.is_file() and self.is_about_tnspack(aboutpath)

###
# prototype::
#     aboutfile = ; // See Python typing...
#                 the path of an ``about.peuf`` file.
#
#     :return: = ; // See Python typing...
#                ``True`` if the ``about.peuf`` indicates a ¨tnslatex package,
#                and ``False`` in other cases.
###
    def is_about_tnspack(self, aboutfile: PPath) -> bool:
        try:
            with ReadBlock(
                content = aboutfile,
                mode    = ABOUT_PEUF_MODE
            ) as datas:
                infos = datas.mydict("std nosep nonb")
    
        except ASTError:
            relpath = aboutfile - self.monorepo
            
            self.new_error(
                src_relpath = relpath,
                info        = f'about file "{relpath}" bad formatted.'
            )
            return False

        if GENE_TAG in infos:
            infos = infos[GENE_TAG]

            return infos.get(GENE_TNSLATEX_TAG, None) == YES_TAG

        return False

###
# This method update ``self.packs_paths`` with the list of the ``PPath`` 
# of the packages changed from the ¨git point of view.
###
    def gitpaths(self) -> None:
        with cd(self.monorepo):
            gitoutput = runthis("git a")

        packstoupdate: List[PPath] = []

        for packpath in self.packs_paths:
            packpath_str = str(packpath - self.monorepo)
            
            if packpath_str in gitoutput:
                packstoupdate.append(PPath(packpath))

        self.packs_paths = packstoupdate