#! /usr/bin/env python3

from enum import Enum

from .spk_interface import *


# -------------- #
# -- STYLISTS -- #
# -------------- #

###
# prototype::
#     value    = ; // See Python typing...
#                the style code choosen.
#     codetemp = ; // See Python typing...
#                a template that will be updated with the vaue of 
#                the color code.
#     normcode = ; // See Python typing...
#                the code for the normal style.
#
# This function is just a basic factorization for the code of the stylists.
###

def _colorit(
    value   : str,
    codetemp: str,
    normcode: str,
) -> None:
    if value:
        termcode = codetemp.format(value = value)

    else:
        termcode = normcode

    print(termcode, end = "")


###
# This class "colorizes" easily the terminal outputs.
###

# Source: GNU/Linux Mag. - Hors Série 115

class ColorStylist(Enum):
# See ``spk_interface.ALL_CONTEXTS.``
    normal :str = ''
    error  :str = '31'
    warning:str = '96'
    good   :str = '94'

    def colorit(self) -> None:
        _colorit(
            value    = self.value,
            codetemp = '\x1b[1;{value}m',
            normcode = '\x1b[0m'
        )

###
# This class uses a "black and white" style for the terminal outputs.
###

class BWStylist(Enum):
# See ``spk_interface.ALL_CONTEXTS.``
    normal :str = ''
    error  :str = 'x'
    warning:str = 'x'
    good   :str = 'x'

    def colorit(self) -> None:
        _colorit(
            value    = self.value,
            codetemp = '\033[1m',
            normcode = '\033[0m'
        )


# ------------------ #
# -- TERM SPEAKER -- #
# ------------------ #

###
# This class implements methods to print ¨infos on the terminal.
###

class TermSpeaker(AbstractSpeaker):
###
# prototype::
#     style = _ in spk_interface.ALL_GLOBAL_STYLES; // See Python typing...
#             a global style for the outputs.
###
    def __init__(
        self,
        style
    ):
        super().__init__(style)

        self.stylist = {
            GLOBAL_STYLE_COLOR: ColorStylist,
            GLOBAL_STYLE_BW   : BWStylist
        }[self.global_style]


###
# prototype::
#     repeat = (1) ; // See Python typing...
#              the numebr of empty lines wanted.
#
# This method simply prints ``repeat`` empty lines on the terminal.
###
    def NL(self, repeat: int = 1) -> None:
        print("\n"*(repeat - 1))

###
# prototype::
#     message = ; // See Python typing...
#               the message to print on the terminal.
#     tab     = (""); // See Python typing...
#               a possible tabulation to use for each new line created.
#     nowrap  = (False); // See Python typing...
#               ``True`` avoids the hard wrapping and otherwise 
#               ``False`` asks to use the hard wrapping.
#
# warning::
#     The arguments ``tab`` and ``nowrap`` are not used with the terminal 
#     speaker but we have to use a general API to make feel us happy when
#     coding (this arguments are used by ``log.LogSpeaker``).
###
    def print(
        self,
        message: str,
        tab    : str = "",
        nowrap : bool = False
    ) -> None:
        print(message)

###
# prototype::
#     context = _ in spk_interface.CONTEXTS (interface.CONTEXT_NORMAL) ; // See Python typing...
#               a context to format some outputs
#
#     see = ``ColorStylist`` and ``BWStylist``.
###
    def style(self, context: str = CONTEXT_NORMAL) -> None:
        getattr(self.stylist, context).colorit()
