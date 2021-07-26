#! /usr/bin/env python3

from typing import *

from collections import defaultdict

from mistool.os_use import PPath, cd, runthis
from mistool.string_use import between

from orpyste.data import ReadBlock, PeufError

from .config    import *
from .logit     import *
from .finalprod import *
from .problems  import *


# ----------- #
# -- TOOLS -- #
# ----------- #

###
# prototype::
#     onepath = ; // See Python typing...
#               a path of a file or a directory.
#     kind    = _ in [DIR_TAG, FILE_TAG]; // See Python typing...
#               the kind of infos wanted.
#
#     return  = ; // See Python typing...
#               ``True`` for a file or a directory to keep and
#               ``False`` in the opposite case.
###

def keepthis(
    onepath: PPath,
    kind   : bool
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
# This class is used by classes analyzing directories.
###

class AnaDir:
###
# prototype::
#     monorepo   = ; // See Python typing...
#                  the path of the directory of the monorepo to explore.
#     dirpath    = ; // See Python typing...
#                  the path of one package to build or update.
#     stepprints = ; // See Python typing...
#                  the functions used to print ¨infos in the terminal.
#     logfile    = ; // See Python typing...
#                  the path of the log file.
#     needabout  = ; // See Python typing...
#                  ``True`` allows that ``about.peuf`` is missing,
#                  contrary to ``False``.
###
    def __init__(
        self,
        monorepo  : PPath,
        dirpath   : PPath,
        stepprints: List[Callable[[str], None]],
        logfile   : PPath,
        needabout : bool = False
    ) -> None:
        self.monorepo   = monorepo
        self.dirpath    = dirpath
        self.stepprints = stepprints
        self.logfile    = logfile
        self.needabout  = needabout

        self.dir_relpath = dirpath - monorepo
        self.logger      = Logger(logfile)

        self.problems  = Problems(self)
        self.finalprod = FinalProd(self)


###
# prototype::
#     context    = _ in [MESSAGE_ERROR, MESSAGE_WARNING]; // See Python typing...
#                  the kind of problem.
#     message    = ; // See Python typing...
#                  the error message to append to the log file.
#     pb_nb      = ; // See Python typing...
#                  the number of the problem.
#     level_term = (1) ; // See Python typing...
#                  the numer of tbabulation to use.
###
    def new_pb(
        self,
        context   : str,
        message   : str,
        pb_nb     : int,
        level_term: int = 1
    ) -> None:
        self.terminfo(
            message = f'{context}: {message}.',
            level   = level_term - 1
        )
        
        self.logger.newpb(
            context = context,
            pb_nb   = pb_nb,
            message = message
        )


###
# prototype::
#     message = ; // See Python typing...
#               the message to append to the log file.
#     isitem  = ; // See Python typing...
#               ``True`` indicates to print an item and
#               ``False`` to no do that. 
#     isnewdir = ; // See Python typing...
#                ``True`` when starting to work on an new
#                folder and ``False`` in other cases.
#     level    = (0); // See Python typing...
#                the level of indentation.
###
    def loginfo(
        self,
        message : str,
        isitem  : bool = False,
        isnewdir: bool = False,
        level   : int  = 0
    ) -> None:
        if isitem:
            message = self.logger.itemize(
                message = message,
                level   = level
            )

            if isnewdir:
                self.logger.NL()

        else:
            self.logger.NL()

        self.logger.appendthis(message)
        self.logger.NL()

###
# prototype::
#     message = ; // See Python typing...
#               the error message to print in the terminal.
#     level   = ; // See Python typing...
#               the level of indentation.
###
    def terminfo(
        self,
        message: str,
        level  : int = 0
    ) -> None:
        self.stepprints[level](message)
