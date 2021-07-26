#! /usr/bin/env python3

from enum import Enum

from mistool.os_use import PPath


# ----------- #
# -- TOOLS -- #
# ----------- #

###
# This class colorize easily the terminal outputs.
###

# Source: GNU/Linux Mag. - Hors Série 115
class ColorTerm(Enum):
    normal :str = ''
    error  :str = '31'
    warning:str = '34'
    OK     :str = '36'

    def colorit(self) -> None:
        if self.value:
            termcode = f"\x1b[1;{self.value}m"

        else:
            termcode = f"\x1b[0m"

        print(termcode, end = "")


# ---------------- #
# -- MAIN CLASS -- #
# ---------------- #

###
# This class implements methiods to print ¨infos on the terminal.
###

class TermSpeaker:

###
# prototype::
#     repeat = (1) ; // See Python typing...
#              the numebr of empty lines wanted.
#
# This method simply prints empty new lines in the terminal.
###
    def term_NL(self, repeat:int = 1) -> None:
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
    def term_print(
        self,
        message: str,
        tab    : str = ""
    ) -> None:
        print(message)
