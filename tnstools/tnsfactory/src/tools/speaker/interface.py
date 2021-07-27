#! /usr/bin/env python3

from abc import ABCMeta, abstractmethod


# --------------- #
# -- CONSTANTS -- #
# --------------- #

CONTEXT_NORMAL = "normal"

CONTEXTS = [
    "error",
    "warning",
    "good",
    CONTEXT_NORMAL,
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
        return (
            hasattr(subclass, 'print') and 
            callable(subclass.print) 
            and 
            hasattr(subclass, 'NL') and 
            callable(subclass.NL)
        )

# We need an attribut for numbered steps.
    def __init__(self):
        self.nb_step = 0

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
#     context = _ in CONTEXTS (CONTEXT_NORMAL) ; // See Python typing...
#               a context for formatting ¨infos.
#
#
# info::
#     This method can't be omitted.
###
    def style(self, context: str = CONTEXT_NORMAL) -> None:
        ...
