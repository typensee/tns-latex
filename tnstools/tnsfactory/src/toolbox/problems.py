#! /usr/bin/env python3

# texplate
# beaulivre
# PyLuaTeX

from collections import defaultdict

from natsort import natsorted

from mistool.os_use import PPath

from .speaker import *


# -------------- #
# -- PROBLEMS -- #
# -------------- #

###
# This class is used to store ¨infos about errors and warnings emitted 
# during all the process.
#
# warning::
#     This class must work whatever the context of use is!
###

class Problems:
###
# prototype::
#     speaker = ; // See Python typing...  
#               an instance of ``toolbox.speaker.allinone.Speaker`` 
#               is used to communicate small ¨infos.
###
    def __init__(
        self,
        speaker: Speaker,
    ) -> None:
        self.speaker = speaker

# ---------
# WARNING !
# ---------
# 
# We use the ordered feature of dict suchas to treat warnings before
# errors in the summaries.
        self._problems: dict = {
            CONTEXT_WARNING : defaultdict(list), # Before ERROR and CRITICAL!
            CONTEXT_CRITICAL: defaultdict(list), # Before ERROR!
            CONTEXT_ERROR   : defaultdict(list),
        }

        self.nb_warnings  = 0
        self.nb_criticals = 0
        self.nb_errors    = 0

        self._pb_id = 0


###
# prototype::
#     :return: = ; // See Python typing...
#                ``True`` if at least one warning has been found and
#                ``False` otherwise.
###
    @property
    def warningfound(self) -> bool:
        return self.nb_warnings != 0

###
# prototype::
#     :return: = ; // See Python typing...
#                ``True`` if at least one "critical" has been found and
#                ``False` otherwise.
###
    @property
    def criticalfound(self) -> bool:
        return self.nb_warnings != 0

###
# prototype::
#     :return: = ; // See Python typing...
#                ``True`` if at least one error has been found and
#                ``False` otherwise.
###
    @property
    def errorfound(self) -> bool:
        return self.nb_errors != 0

###
# prototype::
#     :return: = ; // See Python typing...
#                ``True`` if at least on error or one warning has been found and
#                ``False` otherwise.
###
    @property
    def pbfound(self) -> bool:
        return (
            self.warningfound
            or
            self.criticalfound
            or
            self.errorfound
        )

###
# prototype::
#     :return: = ; // See Python typing...
#                ``True`` if there are several warnings and
#                ``False`` otherwise.
###
    @property
    def several_warnings(self) -> bool:
        return self.nb_warnings > 1

###
# prototype::
#     :return: = ; // See Python typing...
#                ``True`` if there are several "criticals" and
#                ``False`` otherwise.
###
    @property
    def several_criticals(self) -> bool:
        return self.nb_criticals > 1

###
# prototype::
#     :return: = ; // See Python typing...
#                ``True`` if there are several erros and
#                ``False`` otherwise.
###
    @property
    def several_errors(self) -> bool:
        return self.nb_errors > 1


###
# prototype::
#     src_relpath = ; // See Python typing...
#                   the path of the source within the warning has been found.
#     info        = ; // See Python typing...
#                   the info explaining the warning.
#     level       = _ in [0..3] (0); // See Python typing...
#                   the level of the step indicating the problem.
###
    def new_warning(
        self,
        src_relpath: PPath,
        info       : str,
        level      : int = 0
    ) -> None:
        self.nb_warnings += 1

        self._new_pb(
            src_relpath = src_relpath,
            context     = CONTEXT_WARNING,
            info        = info,
            level       = level
        )

###
# prototype::
#     src_relpath = ; // See Python typing...
#                   the path of the source within the warning has been found.
#     info        = ; // See Python typing...
#                   the info explaining the "critical".
#     level       = _ in [0..3] (0); // See Python typing...
#                   the level of the step indicating the problem.
###
    def new_critical(
        self,
        src_relpath: PPath,
        info       : str,
        level      : int = 0
    ) -> None:
        self.nb_criticals += 1

        self._new_pb(
            src_relpath = src_relpath,
            context     = CONTEXT_CRITICAL,
            info        = info,
            level       = level
        )

###
# prototype::
#     src_relpath = ; // See Python typing...
#                   the path of the source within the error has been found.
#     info        = ; // See Python typing...
#                   the info explaining the error.
#     level       = _ in [0..3] (0); // See Python typing...
#                   the level of the step indicating the problem.
###
    def new_error(
        self,
        src_relpath: PPath,
        info       : str,
        level      : int = 0
    ) -> None:
        self.nb_errors += 1

        self._new_pb(
            src_relpath = src_relpath,
            context     = CONTEXT_ERROR,
            info        = info,
            level       = level
        )

###
# prototype::
#     src_relpath = ; // See Python typing...
#                   the path of the source within the problem has been found.
#     context     = _ in [speaker.spk_interface.CONTEXT_ERROR, 
#                         speaker.spk_interface.CONTEXT_WARNING] ; 
#                   the kind of problem.
#     info        = ; // See Python typing...
#                   the info explaining the problem.
#     level       = _ in [0..3] (0); // See Python typing...
#                   the level of the step indicating the problem.
###
    def _new_pb(
        self,
        src_relpath: PPath,
        context    : str,
        info       : str,
        level      : int = 2
    ) -> None:
# Let's store the problems internally.
        self._pb_id += 1
        self._problems[context][src_relpath].append(self._pb_id)

# Let's talk to the world...
        self.speaker.problem(
            context     = context,
            info        = info,
            level       = level,
            pb_id       = self._pb_id
        )


###
# This method ask to print two different summaries, one for the terminal
# and another for the log file.
###
    def resume(self) -> None:
        for context, pbs in self._problems.items():
            if not pbs:
                continue

# Header
            total_nb_pbs = getattr(self, f'nb_{context.lower()}s')

            plurial = "S" if total_nb_pbs > 1 else ""

            self.speaker.recipe(
                    context,
                    NL,
                    {VAR_TITLE:
                        f'{total_nb_pbs} {context.upper()}{plurial} FOUND',
                     VAR_LEVEL  : 2,
                     VAR_WITH_NL: False},
            #
                FORTERM,
                    NL,
                    'Look at the log file and/or above for details.',
            )

# The problems (cardinality + refs).
            for onepath_str in natsorted([
                str(p) for p in pbs
            ]):
                this_ctxt_pb_ids = pbs[PPath(onepath_str)]
                nb_this_ctxt_pbs = len(this_ctxt_pb_ids)

                plurial = "s" if nb_this_ctxt_pbs > 1 else ""

                self.speaker.recipe(
                    context,
                    NL,
                    {VAR_STEP_INFO: f'"{onepath_str}"', 
                     VAR_LEVEL    : 1},
                )
                
                self.speaker.recipe(
                    context,
                    {VAR_STEP_INFO: (
                        f'{nb_this_ctxt_pbs} {context}{plurial}.'
                        '\n'
                        f'See #.: {this_ctxt_pb_ids}.'), 
                     VAR_LEVEL    : 2},
                )
