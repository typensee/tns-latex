#! /usr/bin/env python3

from abc import ABCMeta, abstractmethod


# --------------- #
# -- CONSTANTS -- #
# --------------- #

# -- INTERFACE - AUTO CODE - START -- #

CONTEXT_NORMAL  = "normal"
CONTEXT_ERROR   = "error"
CONTEXT_WARNING = "warning"
CONTEXT_GOOD    = "good"

ALL_CONTEXTS = [
    CONTEXT_NORMAL,
    CONTEXT_ERROR,
    CONTEXT_WARNING,
    CONTEXT_GOOD
]

# -- INTERFACE - AUTO CODE - END -- #


GLOBAL_STYLE_COLOR = "color"
GLOBAL_STYLE_BW    = "balck & white"

ALL_GLOBAL_STYLES = [
    GLOBAL_STYLE_COLOR,
    GLOBAL_STYLE_BW,
]


# -------------------------------- #
# -- ABSTRACT / INTERFACE CLASS -- #
# -------------------------------- #

###
# This abtract/interface class defines the common ¨api of the speakers.
###

class AbstractSpeaker(metaclass=ABCMeta):
# Source to have a real interface: 
#     * https://realpython.com/python-interface/#using-abcabcmeta 
    @classmethod
    def __subclasshook__(cls, subclass):
        goodinterface = all(
            hasattr(subclass, methodname) and 
            callable(getattr(subclass, methodname)) 
            for methodname in [
                'print',
                'NL',
            ]
        )

        return goodinterface

###
# prototype::
#     style  = _ in ALL_GLOBAL_STYLES; // See Python typing...
#              a global style for the output. Internally this style is  
#              stored in the attribut ``global_style``.
# 
# warning::
#     An attribut ``nbstep`` is also created: it is used to number 
#     the zero level steps.
###
    def __init__(
        self,
        style: str
    ):
        assert(style in ALL_GLOBAL_STYLES)
        
        self.global_style = style
        self.nbstep       = 0


###
# prototype::
#     message = ; // See Python typing...
#               a message to add as it.
#     tab     = (""); // See Python typing...
#               a possible tabulation to use for each new line created.
#     nowrap  = (False); // See Python typing...
#               ``True`` avoids the hard wrapping and otherwise 
#               ``False`` asks to use the hard wrapping.
#
# info::
#     The argument ``nowrap`` is useful for log files.
###
    @abstractmethod
    def print(
        self,
        message: str,
        tab    : str  = "",
        nowrap : bool = False
    ) -> None:
        raise NotImplementedError

###
# prototype::
#     repeat = (1) ; // See Python typing...
#              the numebr of empty lines wanted.
###
    @abstractmethod
    def NL(self, repeat: int = 1) -> None:
        raise NotImplementedError


###
# This method simpliy resets to `0` the number of numbered steps.
###
    def reset_nbstep(self) -> None:
        self.nbstep = 0

###
# prototype::
#     context = _ in ALL_CONTEXTS (CONTEXT_NORMAL) ; // See Python typing...
#               a context for formatting ¨infos.
#
#
# info::
#     This method doesn't need to be implemented (some speaker has no style 
#     like the log like ones).
###
    def style(self, context: str = CONTEXT_NORMAL) -> None:
# Help for debuging.
#         print(self.__class__)
        ...
