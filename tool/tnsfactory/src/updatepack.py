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
# This class builds or updates a package.
#
# info::
#     Several errors can be printed in the log file. This allows to correct 
#     several problems at the same time.
###

class UpdateOnePack(AnaDir):

###
# prototype::
#     monorepo   = ; # See Python typing...
#                  the path of the directory of the monorepo explored.
#     dirpath    = ; # See Python typing...
#                  the path of one package to build or update.
#     kindwanted = _ in TOC.ALL_USER_KINDS; # See Python typing...
#                  the kind of ¨infos allowed.
#     stepprints = ; # See Python typing...
#                  the functions used to print ¨infos in the terminal.
#     logfile    = ; # See Python typing...
#                  the path of the log file.
###
    def __init__(
        self,
        monorepo  : PPath,
        dirpath   : PPath,
        kindwanted: str,
        stepprints: List[Callable[[str], None]],
        logfile   : PPath
    ) -> None:
        super().__init__(
            monorepo   = monorepo,
            dirpath    = dirpath,
            stepprints = stepprints,
            logfile    = logfile,
            needabout  = True
        )

        self.kindwanted = kindwanted

###
# This method is the bandleader.
###
    def build(self) -> None:
# Let's be optimism.
        self.success = True

# About the package
        self.stepprints[0](MESSAGE_ABOUT + "looking for metainfos.")

        self.about = About(self).build()
        if not self.success:
            return

# List of source dirs.
        NL()
        self.stepprints[0](MESSAGE_SRC + "searching...")

        anascrdir = AnaDir(
            monorepo   = self.monorepo,
            dirpath    = self.dirpath / SRC_DIR_NAME,
            stepprints = self.stepprints,
            logfile    = self.logfile
        )
         
        self.srcdirs = srcdirs(
            anadir     = anascrdir,
            kindwanted = TOC.KIND_DIR
        )
        self.success = anascrdir.success
        if not self.success:
             return

# Let's aanlyze each source dir.
        for onesrcdir in self.srcdirs:
            NL()
            self.stepprints[0](
                MESSAGE_SRC + f'analyzing "{self.dir_relpath / onesrcdir}".'
            )


            # exit()

# No problem met, we can build everything.
        if self.success:
            NL()
            self.stepprints[0](MESSAGE_FINAL_PROD + 'building.')






            


# Final build broken!
            if not self.success:
                CLEANNNNNN

