#! /usr/bin/env python3

from typing import *

from .problems import *
from .timer import *


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
        self.monorepo         = monorepo
        self.monorepo_relpath = PPath(monorepo.name)

        self.problems = problems
        self.success  = True

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
#     :see: = problems.Problems.new_warning
# 
# This method is just an easy-to-use wrapper.
#
# info::
#     The difference between a warning and a critical is that a critical is 
#     a warning that blocks one part of the process but not all the process.
#     It is a kind of weak error or very strong warning.
###
    def new_critical(self, *args, **kwargs):
        self.success = False
        self.problems.new_critical(*args, **kwargs)

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
        self.problems.speaker.recipe(*args, **kwargs)

###
# This method indicates the begin of the work.
###
    def open_session(self) -> None:
# Just say "Hello."
        self.recipe(
                CONTEXT_GOOD,
            #
            FORTERM,
                NL,
                {VAR_TITLE: f'TNS LIKE MONOREPO "{self.monorepo.name}"'},
            #
            FORLOG,
                {VAR_TITLE:
                    f'LOG FILE - TNS LIKE MONOREPO "{self.monorepo.name}"'},
        )

        self.recipe(
        # Title for the start.
            FORTERM,
                {VAR_TITLE: "STARTING THE ANALYSIS", 
                 VAR_LEVEL: 2},
        )

# A time stamp.
        timestamp(
            speaker = self.problems.speaker,
            kind    = "STARTING"
        )

###
# This method first cleans files and dirs created just to analyze
# the monorepo and then indicates the end of the process.
###
    def close_session(self) -> None:
# Summary of the problems met.
        self.resume()

# Just say "Good bye!"
        self.recipe(
                NL,
        # Title for the end.
            FORTERM,
                {VAR_TITLE: "ANALYSIS FINISHED", 
                 VAR_LEVEL: 2},
        )

# A time stamp.
        timestamp(
            speaker = self.problems.speaker,
            kind    = "ENDING",
            with_NL = False
        )