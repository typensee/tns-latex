#!/usr/bin/env python3

from re import X
from mistool.os_use import PPath

from ..problems import *


# ---------------- #
# -- ??? -- #
# ---------------- #

###
# ???
###

class SearchSources:

###
# prototype::
#     monorepo = ; // See Python typing...  
#               the path of the directory of the monorepo.
#     initrepo = ; // See Python typing...  
#                ``True`` forces to work on all packages without using
#                term::``git a`` and False uses git to focus only on
#                recent changes.
#     speaker  = ; // See Python typing...  
#                an instance of ``toolbox.speaker.allinone.Speaker`` 
#                is used to communicate small ¨infos.
#     problems = ; // See Python typing...  
#                an instance of ``toolbox.Problems`` that manages a basic 
#                history of the problems found.
#     srcpaths = ( [] ); // See Python typing...  
#                a list of the source paths to analyze. This argument  
#                can be used when calling ``Update`` after another process 
#                has already found the sources to analyze.
###
    def __init__(
        self,
        monorepo: PPath,
        initrepo: bool,
        speaker : Speaker,
        problems: Problems,
        srcpaths: List[PPath] = [],
    ) -> None:
        self.srcpaths = srcpaths

        self.initrepo         = initrepo
        self.monorepo         = monorepo
        self.monorepo_relpath = PPath(monorepo.name)

        self.speaker  = speaker
        self.problems = problems
        self.success  = None


###
# ???
###
    def search(self) -> None:
# Sources have already been found.
        if self.srcpaths:
            return

# We have to look for sources to analyze.
        actiontodo = "create" if self.initrepo else "update"
        allornot   = "all "   if self.initrepo else ""

        self.recipe(
            FORALL,
                {VAR_STEP_INFO: (
                    f'Looking for {allornot}packages to {actiontodo} '
                    f'(initrepo = {self.initrepo}).')},
        )

        actiontodo = actiontodo.replace("te", "ted")

# No source found.
        if not self.srcpaths:
            self.success = False

            self.new_warning(
                src_relpath = self.monorepo_relpath,
                info        = f'no package found to be {actiontodo}.',
            )

            return

# Sources have been found.
        ...





###
# prototype::
#     see = problems.Problems.new_error
# 
# This method is just an easy-to-use wrapper.
###
    def new_error(self, *args, **kwargs):
        self.success = False
        self.problems.new_error(*args, **kwargs)

###
# prototype::
#     see = problems.Problems.new_warning
# 
# This method is just an easy-to-use wrapper.
###
    def new_warning(self, *args, **kwargs):
        self.problems.new_warning(*args, **kwargs)

###
# prototype::
#     see = problems.Problems.resume
# 
# This method is just an easy-to-use wrapper.
###
    def resume(self, *args, **kwargs):
        self.problems.resume(*args, **kwargs)
