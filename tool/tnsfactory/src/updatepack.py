#! /usr/bin/env python3

from .about       import *
from .common      import *
from .logit       import *
from .findsrcdirs import *
from .toc         import *
    

# ----------- #
# -- TOOLS -- #
# ----------- #

###
# This class updates a package.
#
# info::
#     Several errors can be printed in the log file. This allows to correct 
#     several problems at the same time.
###

class UpdateOnePack(AnaDir):

###
# prototype::
#     monorepo   = ; # See Python typing...
#                  the path of the directory of the monorepo to explore.
#     dirpath    = ; # See Python typing...
#                  the path of one package to build or update.
#     kindwanted = _ in TOC.ALL_USER_KINDS; # See Python typing...
#                  the kind of ¨infos allowed.
#     stepprint  = ; # See Python typing...
#                  the function used to print ¨infos in the terminal.
#     logfile    = ; # See Python typing...
#                  the path of the log file.
###
    def __init__(
        self,
        monorepo  : PPath,
        dirpath   : PPath,
        kindwanted: str,
        stepprint : Callable[[str], None],
        logfile   : PPath
    ) -> None:
        super().__init__(
            monorepo  = monorepo,
            dirpath   = dirpath,
            stepprint = stepprint,
            logfile   = logfile,
            needabout = True
        )

        self.kindwanted = kindwanted

###
# This method is the bandleader.
###
    def build(self) -> None:
# Let's be optimism.
        self.success = True

# About the package
        self.stepprint(ABOUT_MESSAGE + "looking for metainfos.")

        self.about = About(self).build()
        if not self.success:
            return

# List of source dirs.
        self.stepprint("Looking for sources.")

        anascrdir = AnaDir(
            monorepo  = self.monorepo,
            dirpath   = self.dirpath / SRC_DIR_NAME,
            stepprint = self.stepprint,
            logfile   = self.logfile
        )
         
        self.srcdirs = srcdirs(
            anadir     = anascrdir,
            kindwanted = TOC.KIND_DIR
        )
        self.success = anascrdir.success
        if not self.success:
             return

# Let's work on each dir.
        for onesrcdir in self.srcdirs:
            print(onesrcdir) 

