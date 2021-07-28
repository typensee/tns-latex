#! /usr/bin/env python3

from mistool.os_use   import PPath
from mistool.term_use import ALL_FRAMES, withframe

from .log  import *
from .term import *


# -------------- #
# -- DECORATE -- #
# -------------- #

MAX_WIDTH: int = 80

# The zero level item will never be used but is simplifies 
# the coding of the API.
ITEM = [
    f'{" "*(4*i)}{deco}'
    if deco != ' ' else
    ''
    for i, deco in enumerate(" *+-")
]

TAB = [
    4*i
    for i in range(0, 4)
]


ASCII_FRAME = {}

for i in range(1, 3):
    ASCII_FRAME[i] = lambda t: withframe(
        text  = t,
        frame = ALL_FRAMES[f'pyba_title_{i}']
    )


# ------------------ #
# -- FOR RECIPES -- #
# ------------------ #

# -- RECIPES - AUTO CODE - START -- #

FORLOG  = "forlog"
FORTERM = "forterm"
FORALL  = "forall"
NL      = "NL"
STYLE   = "style"
PRINT   = "print"
TITLE   = "title"
STEP    = "step"
PROBLEM = "problem"

ACTIONS_NO_ARG = [
    FORLOG,
    FORTERM,
    FORALL,
    NL,
    STYLE,
]

VAR_STEP_INFO = "step_info"
VAR_TITLE     = "title"
VAR_LEVEL     = "level"
VAR_CONTEXT   = "context"
VAR_INFO      = "info"
VAR_PB_ID     = "pb_id"

# -- RECIPES - AUTO CODE - END -- #


# ------------- #
# -- SPEAKER -- #
# ------------- #

###
# This class is used to "speak": the ¨infos are printed on the terminal 
# and in a log file.
#
# warning::
#     This class must work in any context of use!
###

class Speaker(AbstractSpeaker):
    OUTPUT_LOG  = "log"
    OUTPUT_TERM = "term"
    OUTPUT_ALL  = [OUTPUT_LOG, OUTPUT_TERM]

###
# prototype::
#     logfile = ; // See Python typing...  
#               the path of the log file.
#     style   = _ in spk_interface.ALL_GLOBAL_STYLES; // See Python typing...  
#               the path of the log file.
###
    def __init__(
        self,
        logfile: PPath,
        style  : str
    ):
# Here we do not need the use of ``super().__init__()``.
        self._speakers = {
            self.OUTPUT_LOG : LogSpeaker(
                logfile  = logfile,
                maxwidth = MAX_WIDTH,
                style    = style
            ),
            self.OUTPUT_TERM: TermSpeaker(
                style = style
            ),
        }

        self._outputs = self.OUTPUT_ALL


###
# This method is to use only a "LOG FILE" output.
###
    def forlog(self) -> None:
        self._outputs = [self.OUTPUT_LOG]

###
# This method is to use only a "TERM" output.
###
    def forterm(self) -> None:
        self._outputs = [self.OUTPUT_TERM]

###
# This method is to use only all the outputs.
###
    def forall(self) -> None:
        self._outputs = self.OUTPUT_ALL


###
# prototype::
#     repeat = (1) ; // See Python typing...
#              the numebr of empty lines wanted.
#
# This method simply prints ``repeat`` empty new lines in all the ouputs wanted.
###
    def NL(self, repeat: int = 1) -> None:
        for out in self._outputs:
            self._speakers[out].NL(repeat)

###
# prototype::
#     message = ; // See Python typing...
#               the message to print in the terminal.
#     tab     = (""); // See Python typing...
#               a possible tabulation to use for each new line created.
###
    def print(
        self,
        message: str,
        tab    : str = ""
    ) -> None:
        for out in self._outputs:
            self._speakers[out].print(
                message = message,
                tab     = tab
            )

###
# prototype::
#     context = _ in spk_interface.ALL_CONTEXTS (interface.CONTEXT_NORMAL) ; // See Python typing...
#               a context for formatting ¨infos.
###
    def style(self, context: str = CONTEXT_NORMAL) -> None:
        for out in self._outputs:
            self._speakers[out].style(context)


###
# prototype::
#     title   = ; // See Python typing...
#               the content of the title.
#     level   = _ in [1,2] (1); // See Python typing...
#               the level of the title.
#     with_NL = (True); // See Python typing...
#               ``True`` asks to add a new line after the title and
#               ``False`` to not do this 
#
# info::
#     For example, ``with_NL`` is used to print time stamps in the log file.
###
    def title(self, 
        title  : str,
        level  : int  = 1,
        with_NL: bool = True,
    ) -> None:
        self.print(ASCII_FRAME[level](title))

        if with_NL:
            self.NL()

###
# prototype::
#     step_info  = ; // See Python typing...
#                  one short info.
#     level      = _ in [0..3] (0); // See Python typing...
#                  the level of step indicating where ``0`` is for automatic 
#                  numbered enumerations.
###
    def step(self, 
        step_info: str,
        level    : int = 0,
    ) -> None:
        for out in self._outputs:
            item = self.stepitem(
                out   = out,
                level = level
            )

            self._speakers[out].print(
                message = f'{item}{step_info}',
                tab     = " "*len(item)
            )

###
# prototype::
#     out   = ; // See Python typing...
#             the kind of speaker.
#     level = _ in [0..3] (0); // See Python typing...
#             the level of step indicating where ``0`` is for automatic 
#             numbered enumerations.
###
    def stepitem(
        self,
        out  : str,
        level: int = 0,
    ) -> None:
# Enumeration...
        if level == 0:
            self._speakers[out].nbstep += 1

            return f'{self._speakers[out].nbstep}) '

# Basic item
        return f'{ITEM[level]} '


###
# prototype::
#     context = ; // See Python typing...
#               the context of a problem.
#     pb_id   = ; // See Python typing...
#               the number of the problem.
#     message = ; // See Python typing...
#               the message to print.
#     level    = _ in [0..3] (0); // See Python typing...
#                the level of the step indicating the problem.
###
    def problem(
        self,
        context: str,
        pb_id  : int,
        info   : str,
        level  : int = 0
    ) -> None:
        self.style(context)

        for out in self._outputs:
            item = self.stepitem(
                out   = out,
                level = level
            )

            item_ctxt = f"{item}[ {pb_id} ] {context}: "
            tab       = " "*len(item_ctxt)
    
            self._speakers[out].print(
                message = f'{item_ctxt}{info}',
                tab     = tab
            )

        self.style(CONTEXT_NORMAL)


###
# prototype::
#     *args = ;
#             the classical list of args allowed by Python.
# 
# This method allows to indicate recipes to apply suchas to simplify 
# the "speaking". Here is an exemple of use followed by the actions 
# actualy done (some actions have short version expressions).
#
# python::
#     self.speaker.receipe(
#         SPEAKER_FOR_TERM,
#         SPEAKER_NL,
#         (SPEAKER_TITLE, f'MONOREPO "{self.monorepo.name}"'),
#         {VAR_TITLE: "STARTING THE ANALYSIS", 
#          VAR_LEVEL: 2}, # A short version here!
#     )
#
# This says to do the following actions.
#
# python::
#     self.speaker.forterm()
#     self.speaker.NL()
#     self.speaker.title(f'MONOREPO "{self.monorepo.name}"')
#     self.speaker.title(
#         title = "STARTING THE ANALYSIS",
#         level = 2
#     )
###
    def recipe(self, *args) -> None:
# In most cases, to call the good action with its good arguments we will use: 
# ``getattr(self, action)(*action_args, **action_kwargs)``.
        for action in args:
# An action with no arg.
            if action in ACTIONS_NO_ARG:
                getattr(self, action)()
                continue

# Just a context.
            elif action in ALL_CONTEXTS:
                action_args   = [action]
                action_kwargs = {}  
                action        = STYLE    

# A "string short version" that is not a context: this will just be printed.
            elif type(action) == str:
                self.print(action)
                continue

# A "dict short version": we have to guess the action.
            elif type(action) == dict:
                action_args   = []
                action_kwargs = action   

                if VAR_TITLE in action:
                    action = TITLE

                elif VAR_STEP_INFO in action:
                    action = STEP

                elif VAR_CONTEXT in action:
                    action = PROBLEM

                else:
                    raise ValueError(
                          "impossible to guess the action with the dict:\n"
                        + repr(action)
                    )

# Actions given with args.
            else:
                action_args   = []
                action_kwargs = {}

                action, *extras = action

# ``extras`` is just on dict.
                if (
                    len(extras) == 1 
                    and 
                    type(extras[0]) == dict
                ):
                    action_kwargs = extras[0]

# ``extras`` is a list of args.
                else:
                    action_args = extras

# End of the so clever analysis :-) .
#
# We can call the good action with the good args.
            getattr(self, action)(*action_args, **action_kwargs)
