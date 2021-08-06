#! /usr/bin/env python3

from .search_packs   import *
from .search_sources import *


# ------------- #
# -- UPDATER -- #
# ------------- #

###
# This class manages the different processes need to find all the source codes
# of a monorepo that follows the ¨tns way of coding.
###

class FindAllSources(SearchPacks):
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
#
# info::
#     The sources found will be stored in the dict ``self.src_found`` that 
#     will look like this:
#
#     python::
#         {
#             "name of a package": {
#                  "1st source subdir": [
#                      "list", "of", "source", "files"
#                  ],
#                  "2nd source subdir": [
#                      "another", "list", "of", "sources"
#                  ],
#             }
#         }
###
    def __init__(
        self,
        monorepo: PPath,
        initrepo: bool,
        problems: Problems,
    ) -> None:
        super().__init__(
            monorepo    = monorepo,
            initrepo    = initrepo,
            problems    = problems
        )

        self.src_found: dict = {}


###
# Here is the great bandleader.
###
    def build(self) -> None:
# Let's be optimistic...
        self.success = True

# Let's work.
        for methodname in [
            "search_packs" , # See ``filendir.search_packs.SearchPacks``.
            "analyze_packs",
        ]:
            getattr(self, methodname)()

            if not self.success:
                break


###
# This method builds the dict ``self.src_found`` containing all the source
# codes found (the resources needed for the user ¨doc are not managed here).
###
    def analyze_packs(self) -> None:
        searchcodes = SearchSources(
            monorepo = self.monorepo,
            package  = None,
            problems = self.problems
        )

        self.src_found = {}

        for onepack in self.packs_paths:
            searchcodes.package = onepack
            searchcodes.extract()

            self.src_found[onepack] = defaultdict(list)

            for onepath in searchcodes.src_files:
                srcdir = list(
                    (onepath - (onepack / SRC_DIR_NAME)).parents
                )[-2]

                self.src_found[onepack][srcdir].append(onepath)
