#!/usr/bin/env python3

from .search_base import *
from .toc         import *


# ----------------------------------------------- #
# -- FILE SOURCES OF A SINGLE TNS LIKE PACKAGE -- #
# ----------------------------------------------- #

###
# This class looks for sources insie a ¨tnslatex like package that 
# will be analyzed later.
###

class SearchSources(SearchDirFile):

###
# prototype::
#     monorepo = ; // See Python typing...  
#                the path of the directory of the monorepo.
#     package  = ; // See Python typing...
#                the path of one package to analyze.
#     problems = ; // See Python typing...
#                an instance of ``toolbox.Problems`` that manages 
#                a basic history of the problems found.
###
    def __init__(
        self,
        monorepo: PPath,
        package : PPath,
        problems: Problems,
    ) -> None:
        super().__init__(        
            monorepo = monorepo,
            problems = problems
        )

        self.package = package
        

###
# Here is the big little bandleader.
###
    def extract(self) -> None:
# The attributes used...
        self.relpackage = self.package - self.monorepo
    
        self.src_package    = self.package / SRC_DIR_NAME
        self.src_relpackage = self.src_package - self.monorepo
        
        self.src_dirs       : List[PPath] = []
        self.src_files      : List[PPath] = []
        self._temp_src_files: List[PPath] = []

        self._toc_used = False

# Let's talk to the world.
        self.recipe(
            NL,
            {VAR_STEP_INFO: f'Looking inside "{self.relpackage}".'}
        )

# Let's go!
        for methodname in [
            "find_srcdirs",
            "find_srcfiles",
        ]:
            getattr(self, methodname)()

            if not self.success:
                return


###
# This method updates ``self.src_dirs`` with the list of the source 
# directories found.
###
    def find_srcdirs(self) -> None:
        self.recipe(
            FORTERM,
                {VAR_STEP_INFO: 'Searching for sources...',
                 VAR_LEVEL    : 1},
        )

# Build source dirs.
        self.build_sources(
            onedir   = self.src_package,
            attrname = "src_dirs",
            kind     = DIR_TAG,
            level    = 1
        )


###
# This method analyzes the file sources of the package and prepares the building
# of the final sources.
###
    def find_srcfiles(self) -> None:
        self.src_files = []

        for onesrcdir in self.src_dirs:
            onesrcdir_rel = onesrcdir - self.monorepo
            self.recipe(
                NL,
                {VAR_STEP_INFO: f'Working in "{onesrcdir_rel}".',
                 VAR_LEVEL    : 1},
            )

# Build source files.
            self.build_sources(
                onedir   = onesrcdir,
                attrname = "_temp_src_files",
                kind     = FILE_TAG,
                level    = 2
            )

            if not self.success:
                return
            
            self.src_files += self._temp_src_files

# Local used?
            self.find_locale(
                onedir      = onesrcdir,
                main_reldir = self.package
            )


###
# prototype::
#     onedir      = ; // See Python typing...
#                   a directory where to look for sources given in a about file.
#     main_reldir = ; // See Python typing...
#                   a path of a containing directory.
#
# This method updates ``self.src_files`` with the list of the directories 
# containing files for internationalization.
###
    def find_locale(
        self, 
        onedir     : PPath,
        main_reldir:PPath,
    ):
        localedir = onedir / LOCALE_DIR

        if not localedir.is_dir():
            return
        
        self.recipe(
            FORTERM,
                {VAR_STEP_INFO: '"locale" dir found.',
                VAR_LEVEL    : 2},
        )


        nb_resources = 0

        for onefile in self.reciter_locale_files(
            onedir      = localedir,
            main_reldir = self.package
        ):
            nb_resources += 1

            self.src_files.append(localedir / onefile)


        if nb_resources == 0:
            self.new_warning(
                src_relpath = localedir - self.monorepo,
                info        = 'no resource found in a "locale" dir.',
                level       = 2
            )
        
        else:
            plurial = "" if nb_resources == 1 else "s"
        
            self.recipe(
                {VAR_STEP_INFO: 
                    f'{nb_resources} resource{plurial} found in a "locale" dir.',
                 VAR_LEVEL    : 2},
            )

###
# prototype::
#     onedir      = ; // See Python typing...  
#                   the path of a directory .
#     main_reldir = ; // See Python typing...
#                   a path of a containing directory.
#     firstcall   = ; // See Python typing...  
#                   this is used to ignore the dir path::``translate`` inside 
#                   the dir path::``locale``.
#
#     :return: = ; // See Python typing...
#                this method iterates recursively inside the content of
#                a directory and yields the files wanted.
#
#     :see: = self.is_kept
###
    def reciter_locale_files(
        self, 
        onedir     : PPath, 
        main_reldir: PPath, 
        firstcall  : bool = True
    ) -> Iterator[PPath]:
        for fileordir in onedir.iterdir():
            if fileordir.is_dir():
                if firstcall and fileordir.name == TRANSLATE_DIR:
                    continue

                for onefile in  self.reciter_locale_files(
                    onedir      = fileordir, 
                    main_reldir = main_reldir,
                    firstcall   = False
                ):
                    yield onefile

            elif self.is_kept(
                onepath     = fileordir,
                kind        = FILE_TAG,
                main_reldir = main_reldir
            ):
                yield fileordir
