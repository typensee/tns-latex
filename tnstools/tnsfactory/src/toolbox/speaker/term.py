#! /usr/bin/env python3

from enum import Enum

from .spk_interface import *


# ----------- #
# -- TOOLS -- #
# ----------- #

###
# This class colorize easily the terminal outputs.
###

# Source: GNU/Linux Mag. - Hors Série 115
class ColorStylist(Enum):
# See ``interface.CONTEXTS.``
    normal :str = ''
    error  :str = '31'
    warning:str = '34'
    good   :str = '36'

    def colorit(self) -> None:
        if self.value:
            termcode = f"\x1b[1;{self.value}m"

        else:
            termcode = f"\x1b[0m"

        print(termcode, end = "")


class BWStylist(Enum):
# See ``interface.CONTEXTS.``
    normal :str = ''
    error  :str = 'x'
    warning:str = 'x'
    good   :str = 'x'

    def colorit(self) -> None:
        if self.value:
            termcode = "\033[1m"

        else:
            termcode = "\033[0m"

        print(termcode, end = "")


# ---------------- #
# -- MAIN CLASS -- #
# ---------------- #

###
# This class implements methiods to print ¨infos on the terminal.
###

class TermSpeaker(AbstractSpeaker):
###
# prototype::
#     style = _ in spk_interface.ALL_STYLES; // See Python typing...
#             a global style for the output.
###
    def __init__(
        self,
        style
    ):
        super().__init__(style)

        self.stylist = {
            SPK_GLOBAL_STYLE_COLOR: ColorStylist,
            SPK_GLOBAL_STYLE_BW   : BWStylist
        }[self.global_style]


###
# prototype::
#     repeat = (1) ; // See Python typing...
#              the numebr of empty lines wanted.
#
# This method simply prints some new empty lines in the terminal.
###
    def NL(self, repeat: int = 1) -> None:
        print("\n"*(repeat - 1))

###
# prototype::
#     message = ; // See Python typing...
#               the message to print in the terminal.
#     tab     = (""); // See Python typing...
#               a possible tabulation to use for each new line created.
#
# warning::
#     The tabulation is not used in the terminal (but we have to use 
#     a general API to make feel us happy when coding).
#     The argument tab is used by ``speaker_log.LogSpeaker``.
###
    def print(
        self,
        message: str,
        tab    : str = ""
    ) -> None:
        print(message)

###
# prototype::
#     context = _ in interface.CONTEXTS (interface.CONTEXT_NORMAL) ; // See Python typing...
#               a context implemented via ``ColorTerm``.
###
    def style(self, context: str = CONTEXT_NORMAL) -> None:
        getattr(self.stylist, context).colorit()
