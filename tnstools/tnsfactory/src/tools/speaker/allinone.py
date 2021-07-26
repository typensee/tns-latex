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
    exec(
    f'''
ASCII_FRAME[{i}] = lambda t: withframe(
    text  = t,
    frame = ALL_FRAMES[f'pyba_title_{i}']
)
    ''')

# ------------------ #
# -- FOR RECIEPES -- #
# ------------------ #

SPK_ACTIONS_NO_ARG         = []
SPK_ACTIONS_NO_ARG_ALLOWED = []

for kind, names in {
    "no_arg":[
        "forlog",
        "forterm",
        "forall",
    ],
    "no_arg_allowed":[
        "NL",
    ],
    "arg":[
        "print",
        "title",
        "step",
        "problem",
    ],
    "var":[
        "message",
        "title",
        "level",
        "pb_id",
        "context",
    ],
}.items():
    for onename in names:
        if kind == "var":
            suffix = f'_{kind.upper()}'
        else:
            suffix = ""

        exec(
        f'''
SPK{suffix}_{onename.upper()} = "{onename}"
        ''')

        if kind in ["no_arg", "no_arg_allowed"]:
            exec(
            f'''
SPK_ACTIONS_{kind.upper()}.append("{onename}")
            ''')


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

class Speaker(LogSpeaker, TermSpeaker):
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
        logfile: PPath
    ):
# The MRO makes the use of the init of LogSpekare as expected...
        super().__init__(
            logfile  = logfile,
            maxwidth = MAX_WIDTH
        )

        self._outputs = self.OUTPUT_ALL
        self._nb_step = 0

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
            getattr(self, f'{out}_NL')(repeat)

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
            getattr(self, f'{out}_print')(
                message = message,
                tab     = tab
            )


###
# prototype::
#     title  = ; // See Python typing...
#              the title.
#     level  = _ in [1,2] (1); // See Python typing...
#              the level of of the title.
###
    def title(self, 
        title: str,
        level: int  = 1
    ) -> None:
        self.print(ASCII_FRAME[level](title))
        self.NL()

###
# prototype::
#     message  = ; // See Python typing...
#                one message.
#     level    = _ in [0..3] (0); // See Python typing...
#                the level of step indicating where ``0`` is for automatic 
#                numbered enumerations.
###
    def step(self, 
        message: str,
        level  : int = 0,
    ) -> None:
        item = self.stepitem(level)

        self.print(
            message = f'{item}{message}',
            tab     = " "*len(item)
        )

###
# prototype::
#     level = _ in [0..3] (0); // See Python typing...
#             the level of step indicating where ``0`` is for automatic 
#             numbered enumerations.
###
    def stepitem(self,
        level: int = 0,
    ) -> None:
# Enumeration...
        if level == 0:
            self._nb_step += 1

            return f'{self._nb_step}) '

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
        message: str,
        level  : int = 0
    ) -> None:
        context = f"{self.stepitem(level)}[{pb_id}] {context}: "
        tab     = " "*len(context)
 
 # TODO : focusing via self.style(None par défaut cf log file et remise à zréo sinon ERROR, MESSAGE du ColorTerm)
        self.print(
            message = f'{context}{message}',
            tab     = tab
        )


###
# prototype::
#     *args = ;
#             the classical list of args allowed by Python.
# 
# This method allows to indicate recipes to apply suchas to simplify 
# the "speaking". Here is an exemple of use followed by the actions 
# actualy done.
#
# python::
#     self.speaker.receipe(
#         SPEAKER_FOR_TERM,
#         SPEAKER_NL,
#         (SPEAKER_TITLE, f'MONOREPO "{self.monorepo.name}"'),
#         (SPEAKER_TITLE, {SPK_VAR_TITLE: "STARTING THE ANALYSIS", 
#                          SPK_VAR_LEVEL: 2}),
#     )
#
# This says to do the following actions.

# python::
#     self.speaker.forterm()
#     self.speaker.NL()
#     self.speaker.title(f'MONOREPO "{self.monorepo.name}"')
#     self.speaker.title(
#         title = "STARTING THE ANALYSIS",
#         level = 2
#     )
###
    def receipe(self, *args) -> None:
        for action in args:
# No arg actions.
            if action in SPK_ACTIONS_NO_ARG:
                getattr(self, action)()
                continue
            
# Actions with args.
            action_args = []
            action_kwargs = {}

            if not action in SPK_ACTIONS_NO_ARG_ALLOWED:
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

# Let's call the good actuion.
            getattr(self, action)(*action_args, **action_kwargs)
