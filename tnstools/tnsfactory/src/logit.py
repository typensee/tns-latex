#! /usr/bin/env python3

from .common import *


# ----------- #
# -- TOOLS -- #
# ----------- #

###
# This class can append ¨infos in a log file.
###

class Logger:
    MAX_WIDTH: int = 80

    ITEM_0: str = " "*4 + "-"
    ITEM_1: str = " "*8 + "+"

###
# prototype::
#     logfile = ; # See Python typing...
#               the path of the log file.
###
    def __init__(
        self,
        logfile: PPath
    ) -> None:
        self.logfile: PPath = logfile

###
# prototype::
#     message = ; # See Python typing...
#               the warning message to append to the log file.
###
    def appendthis(self, message) -> None:
        with self.logfile.open(
            encoding = "utf8",
            mode     = "a"
        ) as logfile:
            logfile.write(message)

###
# This method simply print an empty new line.
###
    def NL(self, repeat = 1) -> None:
        self.appendthis("\n"*repeat)

###
# prototype::
#     message = ; # See Python typing...
#               a message that has to be itemized.
#     level   = (0); # See Python typing...
#               the level of indentation.
#
#     return = ; # See Python typing...
#              a message itemized.
###
    def itemize(self, 
        message: str,
        level  : int = 0
    ) -> str:
        item = getattr(self, f'ITEM_{level}')

        return f'{item} {message}'

###
# prototype::
#     context = ; # See Python typing...
#               the context of problem.
#     pb_nb   = ; # See Python typing...
#               the number of the problem.
#     message = ; # See Python typing...
#               the message to append to the log file.
#
#     see = self.error , self.warning
#
# The text is hard wrapped suchas to respect the maximum width given by 
# ``self.MAX_WIDTH``.
###
    def newpb(
        self,
        context: str,
        pb_nb  : int,
        message: str
    ) -> None:
        context = f"{self.ITEM_1} {context} {pb_nb}: "
        tab     = "\n" + " "*len(context)
 
        maxwidth   = self.MAX_WIDTH - len(context)
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
        
        message = context + tab.join(shortlines)
        
# Just add the wrapped message.
        self.appendthis(message)
        self.NL()
