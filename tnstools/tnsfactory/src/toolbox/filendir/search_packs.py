#!/usr/bin/env python3

from .search import *


# ---------------- #
# -- ??? -- #
# ---------------- #

###
# ???
###

class SearchPacks(SearchDirFile):

###
# prototype::
#     monorepo    = ; // See Python typing...  
#                   the path of the directory of the monorepo.
#     initrepo    = ; // See Python typing...  
#                   ``True`` forces to work on all packages without using
#                   term::``git a`` and False uses git to focus only on
#                   recent changes.
#     speaker     = ; // See Python typing...  
#                   an instance of ``toolbox.speaker.allinone.Speaker`` 
#                   is used to communicate small ¨infos.
#     problems    = ; // See Python typing...  
#                   an instance of ``toolbox.Problems`` that manages 
#                   a basic history of the problems found.
#     packs_paths = ( [] ); // See Python typing...  
#                   a list of the source paths to analyze. This argument 
#                   can be used when calling ``Update`` after another 
#                   process has already found the sources to analyze.
###
    def __init__(
        self,
        monorepo   : PPath,
        initrepo   : bool,
        speaker    : Speaker,
        problems   : Problems,
        packs_paths: List[PPath] = [],
    ) -> None:
        super().__init__(        
            monorepo = monorepo,
            speaker  = speaker,
            problems = problems
        )

        self.initrepo    = initrepo
        self.packs_paths = packs_paths


###
# This method manages the search of the ¨tnslatex like packages.
###
    def search(self) -> None:
# Sources have already been found.
        if self.packs_paths:
            return

# We have to look for sources to analyze.
        actiontodo = "create" if self.initrepo else "update"
        allornot   = "all "   if self.initrepo else ""

        self.recipe(
#            FORALL, # Default context.
                {VAR_STEP_INFO: (
                    f'Looking for {allornot}packages to {actiontodo} '
                    f'(initrepo = {self.initrepo}).')},
        )

        actiontodo = actiontodo.replace("te", "ted")

# Let's work.
        self.buildpaths()

# No source found.
        if not self.packs_paths:
            self.success = False

            self.new_warning(
                src_relpath = self.monorepo_relpath,
                info        = f'no package found to be {actiontodo}.',
            )

            return

# Sources have been found.
        nbpacks = len(self.packs_paths)
        plurial = "s" if nbpacks > 1 else ""

        if self.initrepo:
            self.recipe(
#            FORALL, # Default context.
                {VAR_STEP_INFO: (
                    f'Initialize the monorepo:'
                     '\n'
                    f'{nbpacks} package{plurial} '
                     'will be treated.')},
            )

        else:
            self.recipe(
#            FORALL, # Default context.
                {VAR_STEP_INFO: 'Using "git a".'},
            )

            self.gitpaths()

            nbpacks_changed = len(self.packs_paths)

            if nbpacks_changed == 0:
                self.recipe(
#            FORALL, # Default context.
                    {VAR_STEP_INFO: 'No change found.',
                     VAR_LEVEL    : 1},
                )

            else:
                percentage = nbpacks_changed / nbpacks * 100

                self.recipe(
#            FORALL, # Default context.
                    {VAR_STEP_INFO: (
                        f'Number of packages changed = {nbpacks_changed}'
                        f'  -->  {percentage:.2f}%'),
                     VAR_LEVEL: 1},
                )
