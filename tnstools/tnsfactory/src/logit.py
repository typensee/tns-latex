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

    ITEM: str = " "*4 + "- "

###
# prototype::
#     logfile = ; # See Python typing...
#               the path of the log file.
###
    def __init__(
        self,
        logfile: PPath
    ) -> None:
        self.logfile = logfile

###
# prototype::
#     message = ; # See Python typing...
#               the warning message to append to the log file.
###
    def appendtologfile(self, message: str) -> None:
        with self.logfile.open(
            encoding = "utf8",
            mode     = "a"
        ) as logfile:
            logfile.write(message)

###
# This method simply print an empty new line.
###
    def logfile_NL(self) -> None:
        self.appendtologfile("\n")

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
    def logthisinfos(
        self,
        kind   : str,
        message: str
    ) -> None:
        title = f"{self.ITEM}{kind}: "
        tab   = "\n" + " "*len(title)
 
        maxwidth   = self.MAX_WIDTH - len(title)
        shortlines = []

        for block in message.split('\n'):
            block    = [w.strip() for w in block.split(' ')]
            lastline = block.pop(0)
        
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
        
# Just add the wrapped message.
        self.appendtologfile(message)
        self.logfile_NL()

###
# prototype::
#     message = ; # See Python typing...
#               the error message to append to the log file.
###
    def error(self, message: str) -> None:
        self.logthisinfos(self.ERROR, message)

###
# prototype::
#     message = ; # See Python typing...
#               the warning message to append to the log file.
###
    def warning(self, message: str) -> None:
        self.logthisinfos(self.WARNING, message)

