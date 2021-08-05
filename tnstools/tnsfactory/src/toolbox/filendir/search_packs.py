#!/usr/bin/env python3

from mistool.os_use import cd, runthis

from .search_base import *


# ----------------------- #
# -- TNS LIKE PACKAGES -- #
# ----------------------- #

###
# This class looks for ¨tnslatex like packages that will be analyzed later.
###

class SearchPacks(SearchDirFile):

###
# prototype::
#     monorepo = ; // See Python typing...  
#                the path of the directory of the monorepo.
#     initrepo = ; // See Python typing...  
#                ``True`` forces to work on all packages without using
#                term::``git a`` and False uses git to focus only on
#                recent changes.
#     problems = ; // See Python typing...  
#                an instance of ``toolbox.Problems`` that manages 
#                a basic history of the problems found.
###
    def __init__(
        self,
        monorepo: PPath,
        initrepo: bool,
        problems: Problems,
    ) -> None:
        super().__init__(        
            monorepo = monorepo,
            problems = problems
        )

        self.initrepo = initrepo

        self.packs_paths: List[PPath] = []


###
# This method manages the search of the ¨tnslatex like packages.
###
    def search_packs(self) -> None:
# Sources have already been found.
        if self.packs_paths:
            return

# We have to look for sources to analyze.
        actiontodo = "create" if self.initrepo else "update"
        allornot   = "all "   if self.initrepo else ""

        self.recipe(
            {VAR_STEP_INFO: (
                f'Looking for {allornot}packages to {actiontodo} '
                f'(initrepo = {self.initrepo}).')},
        )

        actiontodo = actiontodo.replace("te", "ted")

# Let's work.
        self.build_packpaths()

# No source have been found.
        if not self.packs_paths:
            self.new_critical(
                src_relpath = self.monorepo_relpath,
                info        = f'no package found to be {actiontodo}.',
            )

            return

# Some sources have been found.
        nbpacks = len(self.packs_paths)
        plurial = "s" if nbpacks > 1 else ""

        self.recipe(
            NL
        )

# (Re)create all the existing packages.
        if self.initrepo:
            self.recipe(
                {VAR_STEP_INFO: (
                    f'Initializing the monorepo:'
                     '\n'
                    f'{nbpacks} package{plurial} will be treated.')},
            )

# Just us the git's point of view.
        else:
            self.recipe(
                {VAR_STEP_INFO: 'Using "git a".'},
            )

            self.git_packpaths()

            nbpacks_changed = len(self.packs_paths)

            if nbpacks_changed == 0:
                self.recipe(
                    {VAR_STEP_INFO: 'No change found.',
                     VAR_LEVEL    : 1},
                )

            else:
                percentage = nbpacks_changed / nbpacks * 100

                self.recipe(
                    {VAR_STEP_INFO: (
                        f'Number of packages changed = {nbpacks_changed}'
                        f'  -->  {percentage:.2f}%'),
                     VAR_LEVEL: 1},
                )


###
# This methods builds the sorted list of the ``PPath`` of the ¨tnslatex  
# packages to analyze.
###
    def build_packpaths(self) -> None:
        self.packs_paths = self.recbuild_packpaths(self.monorepo)
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
    def recbuild_packpaths(self, onedir: PPath) -> List[PPath]:
        packsfound: List[PPath] = []

        for subdir in self.iterIOkept(
            onedir      = onedir,
            kind        = DIR_TAG,
            main_reldir = self.monorepo
        ):
            if self.is_pack(subdir):
                packsfound.append(subdir)

            else:
                packsfound += self.recbuild_packpaths(subdir)

        return packsfound


###
# prototype::
#     subdir = ; // See Python typing...
#              the path of a sub directory of the monorepo.
#
#     :return: = ; // See Python typing...
#                ``True`` if the ``about.peuf`` indicates a ¨tnslatex package,
#                and ``False`` in other cases.
###
    def is_pack(self, subdir: PPath) -> bool:
# No about file.
        if not self.has_about(subdir):
            return False

        infos = self.about_content()

# Bad formatted about file!
        if not self.success:
            return

# Good formatting about file.
        if GENE_TAG in infos:
            infos = infos[GENE_TAG]

            return infos.get(GENE_TNSLATEX_TAG, NO_TAG) == YES_TAG

        return False


###
# This method updates ``self.packs_paths`` with the list of the ``PPath`` 
# of the packages changed from the ¨git point of view.
###
    def git_packpaths(self) -> None:
        with cd(self.monorepo):
            gitoutput = runthis("git a")

        packstoupdate: List[PPath] = []

        for packpath in self.packs_paths:
            pack_relpath = str(packpath - self.monorepo)
            
            if pack_relpath in gitoutput:
                packstoupdate.append(PPath(packpath))

        self.packs_paths = packstoupdate
