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

###
# prototype::
#     updater = updatepack.UpdateOnePack ; 
#               the instance used to update one package. 
###
    def __init__(
        self,
        updater# Can't us the type UpdateOnePack (cyclic imports).
    ) -> None:
        self.logfile     = updater.logfile
        self.dir_relpath = updater.dir_relpath

###
# prototype::
#     kind    = _ in [self.ERROR, self.WARNING] ; # See Python typing...
#               the kind of message.
#     message = ; # See Python typing...
#               the message to append to the log file.
#
#     see = self.error , self.warning
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
            logfile.write(f'\n"{self.dir_relpath}" - {kind}: {message}')

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
