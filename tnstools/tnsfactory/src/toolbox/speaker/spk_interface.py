#! /usr/bin/env python3

from abc import ABCMeta, abstractmethod


# --------------- #
# -- CONSTANTS -- #
# --------------- #

# -- INTERFACE - AUTO CODE - START -- #

CONTEXT_NORMAL = "normal"
CONTEXT_ERROR = "error"
CONTEXT_WARNING = "warning"
CONTEXT_GOOD = "good"

ALL_CONTEXTS = [
    CONTEXT_NORMAL,
    CONTEXT_ERROR,
    CONTEXT_WARNING,
    CONTEXT_GOOD
]

# -- INTERFACE - AUTO CODE - END -- #


GLOBAL_STYLE_COLOR = "color"
GLOBAL_STYLE_BW    = "balck & white"

GLOBAL_ALL_STYLES = [
    GLOBAL_STYLE_COLOR,
    GLOBAL_STYLE_BW,
]


# ---------------- #
# -- MAIN CLASS -- #
# ---------------- #

###
# This class ???
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
#     style  = _ in ALL_STYLES; // See Python typing...
#              a global style for the output. Internally this style is stored 
#              in the attribut ``global_style``.
# 
# warning::
#     An attribut ``nbstep`` is created: it is for the first level 
#     numbered steps.
###
    def __init__(
        self,
        style: str
    ):
        assert(style in GLOBAL_ALL_STYLES)
        
        self.global_style = style
        self.nbstep       = 0


###
# prototype::
#     message = ; // See Python typing...
#               a message to be hard wrapped.
#     tab     = (""); // See Python typing...
#               a possible tab to us each a new line is created.
#     nowrap  = (False); // See Python typing...
#               ``True`` avoids the hard wrapping which is needed for
#               for ``self.log_NL``, and otherwise False asks to use
#               the hard wrapping.
###
    @abstractmethod
    def print(
        self,
        message: str,
        tab    : str = "",
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
# prototype::
#     context = _ in ALL_CONTEXTS (CONTEXT_NORMAL) ; // See Python typing...
#               a context for formatting ¨infos.
#
#
# info::
#     This method do not need to be implemented.
###
    def style(self, context: str = CONTEXT_NORMAL) -> None:
# Help for debuging.
#         print(self.__class__)
        ...


###
# This method reset the number of numbered steps.
###
    def reset_nbstep(self) -> None:
        self.nbstep = 0
