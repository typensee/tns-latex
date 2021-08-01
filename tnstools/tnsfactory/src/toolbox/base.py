#! /usr/bin/env python3

from typing import *

from .problems import *


# ------------------------------ #
# -- BASE COMMUNICATING CLASS -- #
# ------------------------------ #

###
# This class gives the common interface for classes working with "speakers" 
# and "problems".
###

class BaseCom:

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
        self.monorepo         = monorepo
        self.monorepo_relpath = PPath(monorepo.name)

        self.speaker  = speaker
        self.problems = problems
        self.success  = None


###
# prototype::
#     :see: = problems.Problems.new_warning
# 
# This method is just an easy-to-use wrapper.
###
    def new_critical(self, *args, **kwargs):
        self.problems.new_critical(*args, **kwargs)

###
# prototype::
#     :see: = problems.Problems.new_warning
# 
# This method is just an easy-to-use wrapper.
###
    def new_warning(self, *args, **kwargs):
        self.problems.new_warning(*args, **kwargs)

###
# prototype::
#     :see: = problems.Problems.new_error
# 
# This method is just an easy-to-use wrapper.
###
    def new_error(self, *args, **kwargs):
        self.success = False
        self.problems.new_error(*args, **kwargs)

###
# prototype::
#     :see: = problems.Problems.resume
# 
# This method is just an easy-to-use wrapper.
###
    def resume(self, *args, **kwargs):
        self.problems.resume(*args, **kwargs)


###
# prototype::
#     :see: = speaker.allinone.Speaker.recipe
# 
# This method is just an esay-to-use wrapper.
###
    def recipe(self, *args, **kwargs) -> None:
        self.speaker.recipe(*args, **kwargs)
