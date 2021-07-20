#! /usr/bin/env python3

from .common import *


# ----------- #
# -- TOOLS -- #
# ----------- #

###
# This class can append ¨infos in a log file.
###

class Logger:
    ERROR  :str = "ERROR"
    WARNING:str = "WARNING"

    MAX_WIDTH: int = 80

###
# prototype::
#     anadir = common.AnaDir ; 
#              the instance used to update one package. 
###
    def __init__(
        self,
        anadir# Can't use the type common.AnaDir (cyclic imports).
    ) -> None:
        self.logfile     = anadir.logfile
        self.dir_relpath = anadir.dir_relpath

###
# prototype::
#     kind    = _ in [self.ERROR, self.WARNING] ; # See Python typing...
#               the kind of message.
#     message = ; # See Python typing...
#               the message to append to the log file.
#
#     see = self.error , self.warning
#
# The text is hard wrapped suchas to respect the maximum width given by 
# ``self.MAX_WIDTH``.
###
    def addtologfile(
        self,
        kind   : str,
        message: str
    ) -> None:
        with self.logfile.open(
            encoding = "utf8",
            mode     = "a"
        ) as logfile:
            logfile.write(self._hardwrap(kind, message))

###
# prototype::
#     kind    = _ in [self.ERROR, self.WARNING] ; # See Python typing...
#               the kind of message.
#     message = ; # See Python typing...
#               the message to append to the log file.
#
#     return = ; # See Python typing...
#               the message hard wrapped.
###
    def _hardwrap(
        self,
        kind   : str,
        message: str
    ) -> str:
        title = f'\n"{self.dir_relpath}" - {kind}: '
        tab   = "\n" + " "*len(title)
 
        maxwidth   = self.MAX_WIDTH - len(title)
        shortlines = []

        for block in message.split('\n'):
            block   = [w.strip() for w in block.split(' ')]
            lastline  = ""
        
            while(block):
                word = block.pop(0)

                len_lastline = len(lastline)
                len_word     = len(word)

                if len_lastline + len_word > maxwidth:
                    shortlines.append(lastline)
                    lastline = word

                else:
                    lastline += " "+ word

            if lastline:
                shortlines.append(lastline)

        message = title + tab.join(shortlines)
        
        return message

###
# prototype::
#     message = ; # See Python typing...
#               the error message to append to the log file.
###
    def error(self, message: str) -> None:
        self.addtologfile(self.ERROR, message)

###
# prototype::
#     message = ; # See Python typing...
#               the warning message to append to the log file.
###
    def warning(self, message: str) -> None:
        self.addtologfile(self.WARNING, message)
