#! /usr/bin/env python3

from mistool.os_use import PPath

from .spk_interface import *


# ----------------- #
# -- LOG SPEAKER -- #
# ----------------- #

###
# This class implements methods to print ¨infos in the log file.
###

class LogSpeaker(AbstractSpeaker):
###
# prototype::
#     logfile  = ; // See Python typing...  
#                the path of the log file.
#     style    = _ in spk_interface.ALL_GLOBAL_STYLES; // See Python typing...
#                a global style for the outputs.
#     maxwidth = ; // See Python typing...
#                the maw width expected for hard wrapped contents.
###
    def __init__(
        self,
        logfile : PPath,
        style   : str,
        maxwidth: int,
    ) -> None:
        super().__init__(
            style    = style,
            maxwidth = maxwidth
        )

        self.logfile = logfile

        self.reset_logfile()

###
# This method produces a new empty log file.
###
    def reset_logfile(self) -> None:
# Empty an existing log file.
        if self.logfile.is_file():
            with self.logfile.open(
                encoding = "utf8",
                mode     = "w"
            ) as logfile:
                logfile.write("")

# New log file if it doesn't exist.
        else:
            self.logfile.touch()


###
# prototype::
#     text = ; // See Python typing...
#            a text to print as it in the log file.
###
    def print(
        self, text  : str,
    ) -> None:
        with self.logfile.open(
            encoding = "utf8",
            mode     = "a"
        ) as logfile:
            logfile.write(text)
            logfile.write("\n")


###
# prototype::
#     repeat = (1) ; // See Python typing...
#              the numebr of empty lines wanted.
#
# This method simply append ``repeat`` empty new lines to the log file.
###
    def NL(self, repeat: int = 1) -> None:
        self.print("\n"*(repeat - 1))
