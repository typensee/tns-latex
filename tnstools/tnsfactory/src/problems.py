#! /usr/bin/env python3

from sys import settrace
from .common import *


# ----------- #
# -- TOOLS -- #
# ----------- #

###
# This class is used to store ¨infos about errors and warnings emitted.
###

class Problems:
###
# prototype::
#     anadir = common.AnaDir ;  
#              any class having the ¨api of ``common.AnaDir``.
###
    def __init__(
        self,
        anadir,# Can't use the type common.AnaDir (cyclic imports).
    ):
        self.anadir = anadir
        
# We use the ordered feature of dict suchas to treat warnings before
# errors in the summaries.
        self._problems: dict = {
            MESSAGE_WARNING: defaultdict(list), # Before ERROR!
            MESSAGE_ERROR  : defaultdict(list), # After WARNING!
        }

        self._pb_nb       = 0
        self._nb_of_errs  = 0
        self._nb_of_warns = 0

###
# prototype::
#     retun = ; # See Python typing...
#             ``True`` if at least one error has been found and
#             ``False` otherwise.
###
    def errorfound(self) -> bool:
        return bool(self._problems[MESSAGE_ERROR])

###
# prototype::
#     retun = ; # See Python typing...
#             ``True`` if at least on error or one warning has been
#             found and ``False` otherwise.
###
    def pbfound(self) -> bool:
        return (
            self.errorfound()
            or
            bool(self._problems[MESSAGE_WARNING])
        )

###
# prototype::
#     src_relpath = ; # See Python typing...
#                   the path of the source within the problem has been found.
#     context     = _ in [MESSAGE_ERROR, MESSAGE_WARNING] ; # See Python typing...
#                   the kind of problem.
#     message     = ; # See Python typing...
#                   the message explaining the problem.
#     level_term  = (1) ; # See Python typing...
#                   the numer of tbabulation to use.
###
    def _new_pb(
        self,
        src_relpath: PPath,
        context    : str,
        message    : str,
        level_term : int = 2
    ) -> None:
        self._pb_nb += 1

        self.anadir.new_pb(
            context    = context,
            message    = message,
            level_term = level_term,
            pb_nb      = self._pb_nb
        )

        self._problems[context][src_relpath].append(self._pb_nb)

###
# prototype::
#     src_relpath = ; # See Python typing...
#                   the path of the source within the error has been found.
#     message     = ; # See Python typing...
#                   the message explaining the error.
#     level_term  = (1) ; # See Python typing...
#                   the numer of tbabulation to use.
###
    def new_error(
        self,
        src_relpath: PPath,
        message    : str,
        level_term : int = 2
    ):
        self._nb_of_errs += 1

        self._new_pb(
            src_relpath = src_relpath,
            context     = MESSAGE_ERROR,
            message     = message,
            level_term  = level_term
        )

###
# prototype::
#     src_relpath = ; # See Python typing...
#                   the path of the source within the warning has been found.
#     message     = ; # See Python typing...
#                   the message explaining the warning.
#     level_term  = (1) ; # See Python typing...
#                   the numer of tbabulation to use.
###
    def new_warning(
        self,
        src_relpath: PPath,
        message    : str,
        level_term : int = 2
    ):
        self._nb_of_warns += 1

        self._new_pb(
            src_relpath = src_relpath,
            context     = MESSAGE_WARNING,
            message     = message,
            level_term  = level_term
        )


###
# prototype::
#     return = ; # See Python typing...
#              ``True`` if there several erros and ``False`` otherwise.
###
    @property
    def several_warnings(self) -> bool:
        return self._nb_of_warns != 1

###
# prototype::
#     return = ; # See Python typing...
#              ``True`` if there several erros and ``False`` otherwise.
###
    @property
    def several_errors(self) -> bool:
        return self._nb_of_errs != 1

###
# This method ask to print two different summaries, one for the terminal
# and another for the log file.
###
    def resume(self) -> None:
        for kind, pbs in self._problems.items():
            if not pbs:
                continue

            if kind == MESSAGE_ERROR:
                colorize = ColorTerm.error.colorit
            else:
                colorize = ColorTerm.warning.colorit

# Title
            if getattr(self, f'several_{kind.lower()}s') == True:
                before  = "SEVERAL "
                plurial = "S"
    
            else:
                before  = "ONE "
                plurial = ""

            title = ASCII_FRAME_2(f"{before}{kind}{plurial} FOUND")

            colorize()
            NL(2)
            print(title)
            NL(2)
            print(
                'Look at the log file '
                f'"{self.anadir.logfile - self.anadir.monorepo}"'
                ' for details.'
            )
            NL()

            self.anadir.loginfo(title)
            self.anadir.logNL()

# The paths and the numbers of their problems.
            for relpath in sorted(pbs):
                list_nb_pbs = pbs[relpath]


                relpath_str =  f'"{relpath}"'

                colorize()
                self.anadir.terminfo(relpath_str)

                self.anadir.loginfo(
                    message = relpath_str, 
                    isitem  = True
                )


                nb_pbs  = len(list_nb_pbs)
                plurial = "" if nb_pbs == 1 else "s"

                message = f'{nb_pbs} {kind}{plurial} found.'

                colorize()
                self.anadir.terminfo(
                    message = message, 
                    level   = 1
                )

                message += f' See {kind.lower()}{plurial} {list_nb_pbs}.'
                
                self.anadir.loginfo(
                    message = message, 
                    isitem  = True,
                    level   = 1
                )
                
        ColorTerm.normal.colorit()
