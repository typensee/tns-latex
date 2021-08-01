#!/usr/bin/env python3

from .search import *


# ---------------- #
# -- ??? -- #
# ---------------- #

###
# ???
###

class SearchCodes(SearchDirFile):

###
# prototype::
#     monorepo    = ; // See Python typing...  
#                   the path of the directory of the monorepo.
#     package     = ; // See Python typing...  
#                   the path of one package to analyze.
#     speaker     = ; // See Python typing...  
#                   an instance of ``toolbox.speaker.allinone.Speaker`` 
#                   is used to communicate small ¨infos.
#     problems    = ; // See Python typing...  
#                   an instance of ``toolbox.Problems`` that manages 
#                   a basic history of the problems found.
###
    def __init__(
        self,
        monorepo   : PPath,
        package    : PPath,
        speaker    : Speaker,
        problems   : Problems,
    ) -> None:
        super().__init__(        
            monorepo = monorepo,
            speaker  = speaker,
            problems = problems
        )

        self.package = package

