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

SPK_FORLOG = "forlog"
SPK_FORTERM = "forterm"
SPK_FORALL = "forall"
SPK_NL = "NL"
SPK_STYLE = "style"
SPK_PRINT = "print"
SPK_TITLE = "title"
SPK_STEP = "step"
SPK_PROBLEM = "problem"
SPK_VAR_STEP_INFO = "step_info"
SPK_VAR_TITLE = "title"
SPK_VAR_LEVEL = "level"
SPK_VAR_CONTEXT = "context"
SPK_VAR_INFO = "info"
SPK_VAR_PB_ID = "pb_id"

SPK_ACTIONS_NO_ARG = [
    SPK_FORLOG,
    SPK_FORTERM,
    SPK_FORALL,
    SPK_NL,
    SPK_STYLE,
]


SPK_STYLE_NORMAL = CONTEXT_NORMAL
SPK_STYLE_ERROR = CONTEXT_ERROR
SPK_STYLE_WARNING = CONTEXT_WARNING
SPK_STYLE_GOOD = CONTEXT_GOOD

SPK_ALL_STYLES = ALL_CONTEXTS

# -- RECIPES - AUTO CODE - END -- #


# ---------------- #
# -- MAIN CLASS -- #
# ---------------- #

###
# This class is used to "speak": ¨infos are printed on the terminal and 
# in a log file.
#
# warning::
#     This class must work whatever the context of use!
###

class Speaker(AbstractSpeaker):
    OUTPUT_LOG  = "log"
    OUTPUT_TERM = "term"
    OUTPUT_ALL  = [OUTPUT_LOG, OUTPUT_TERM]

###
# prototype::
#     logfile = ; // See Python typing...  
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
# This method sets an only "LOG FILE" output.
###
    def forlog(self) -> None:
        self._outputs = [self.OUTPUT_LOG]

###
# This method sets an only "TERM" output.
###
    def forterm(self) -> None:
        self._outputs = [self.OUTPUT_TERM]

###
# This method sets all the outputs.
###
    def forall(self) -> None:
        self._outputs = self.OUTPUT_ALL


###
# prototype::
#     repeat = (1) ; // See Python typing...
#              the numebr of empty lines wanted.
#
# This method simply prints empty new lines in the ouputs wanted.
###
    def NL(self, repeat = 1) -> None:
        for out in self._outputs:
            self._speakers[out].NL(repeat)

###
# prototype::
#     message = ; // See Python typing...
#               the message to print in the terminal.
#     tab     = (""); // See Python typing...
#               a possible tabulation to use for each new line created.
#
# info::
#     This method will be helpful when using several speakers.
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
#     context = _ in interface.CONTEXTS (interface.CONTEXT_NORMAL) ; // See Python typing...
#               a context for formatting ¨infos.
###
    def style(self, context: str = CONTEXT_NORMAL) -> None:
        for out in self._outputs:
            self._speakers[out].style(context)


###
# prototype::
#     title   = ; // See Python typing...
#               the title.
#     level   = _ in [1,2] (1); // See Python typing...
#               the level of of the title.
#     with_NL = (False); // See Python typing...
#               this allows to not add a new line after the title 
#               (this is used for time stamps in the log file).
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
#               the message to append to the log file.
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

        self.style(SPK_STYLE_NORMAL)


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
#         {SPK_VAR_TITLE: "STARTING THE ANALYSIS", 
#                          SPK_VAR_LEVEL: 2}, # A short version here!
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
        for action in args:
# No arg actions.
            if action in SPK_ACTIONS_NO_ARG:
                getattr(self, action)()
                continue

# Just a style.
            if action in SPK_ALL_STYLES:
                action_args   = [action]
                action_kwargs = {}  
                action        = SPK_STYLE    

# A string short version just to print.
            elif type(action) == str:
                self.print(action)
                continue

# A dict short version: we have to guess the action.
            elif type(action) == dict:
                action_args   = []
                action_kwargs = action   

                if SPK_VAR_TITLE in action:
                    action = SPK_TITLE

                elif SPK_VAR_STEP_INFO in action:
                    action = SPK_STEP

                elif SPK_VAR_CONTEXT in action:
                    action = SPK_PROBLEM

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

# Let's call the good action.
            getattr(self, action)(*action_args, **action_kwargs)
