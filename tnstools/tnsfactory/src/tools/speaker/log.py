#! /usr/bin/env python3

from mistool.os_use import PPath

from .interface import *


# ---------------- #
# -- MAIN CLASS -- #
# ---------------- #

###
# This class implements methiods to print ¨infos in the log file.
###

class LogSpeaker(AbstractSpeaker):
###
# prototype::
#     logfile  = ; // See Python typing...  
#                the path of the log file.
#     maxwidth = ; // See Python typing...  
#                the maximum number of characters on the same line.
###
    def __init__(
        self,
        logfile : PPath,
        maxwidth: int
    ):
        super().__init__()

        self.logfile  = logfile
        self.maxwidth = maxwidth

        self.reset_logfile()

###
# This method produces a new empty log file.
###
    def reset_logfile(self):
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
#     message = ; // See Python typing...
#               a message to be hard wrapped.
#     tab     = (""); // See Python typing...
#               a possible tabulation to use for each new line created.
#
#     return = ; // See Python typing...
#              a wrapped message of maximal width ``self.maxwidth``.
#
# info::
#     The method works on single lines so if the message uses back returns,
#     thoses ones will be respected.
###
    def hardwrap(
        self,
        message: str,
        tab    : str = ""
    ) -> str:
        shortlines = []

        for block in message.split('\n'):
            block    = [w.strip() for w in block.split(' ')]
            lastline = block.pop(0)
        
            while(block):
                word = block.pop(0)

                len_lastline = len(lastline)
                len_word     = len(word)

                if len_lastline + len_word >= self.maxwidth :
                    shortlines.append(lastline)
                    lastline = tab + word

                else:
                    lastline += " " + word

            if lastline:
                shortlines.append(lastline)
        
        return "\n".join(shortlines)


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
        with self.logfile.open(
            encoding = "utf8",
            mode     = "a"
        ) as logfile:
            if nowrap:
                logfile.write(message)

            else:
                logfile.write(
                    self.hardwrap(
                        message = message,
                        tab     = tab
                    )
                )
# Hard wrapping stripes the message...
                logfile.write("\n")

###
# prototype::
#     repeat = (1) ; // See Python typing...
#              the numebr of empty lines wanted.
#
# This method simply append an empty new line to the log file.
###
    def NL(self, repeat: int = 1) -> None:
        self.print(
            message = "\n"*repeat,
            nowrap  = True
        )
