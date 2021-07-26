#! /usr/bin/env python3

from mistool.os_use import PPath


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

class AbstractSpeaker:
    def __init__(self):
# This attribut will be used for numbered steps.
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
    def print(
        self,
        message: str,
        tab    : str = "",
        nowrap : bool = False
    ) -> None:
        raise NotImplementedError()

###
# prototype::
#     repeat = (1) ; // See Python typing...
#              the numebr of empty lines wanted.
###
    def NL(self, repeat: int = 1) -> None:
        raise NotImplementedError()

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
