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
#     kind       = _ in TOC.ALL_USER_KINDS; # See Python typing...
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
        kind      : str,
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

        self.kind = kind

###
# Here is the great bandleader.
###
    def build(self) -> None:
# Let's be optimism.
        self.success = True

# About the package
        self.stepprints[0](MESSAGE_ABOUT + "looking for metainfos.")
        
        self.loginfo(f'Working on "{self.dir_relpath}"...')

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
            kind = TOC.KIND_DIR
        )
        self.success = anascrdir.success
        if not self.success:
             return

# Let's aanlyze each source dir.
        for onesrcdir in self.srcdirs:
            onesrcpath = self.dirpath / SRC_DIR_NAME / onesrcdir

            NL()

# Does the dir exist?
            if not onesrcpath.is_dir():
                message = f'missing dir "{self.dir_relpath / onesrcdir}"'

                self.stepprints[0](f'{MESSAGE_PROBLEM}: {message}.')
                self.error(message)
                
                continue

# The dir exists.
            self.stepprints[0](
                MESSAGE_SRC + f'analyzing "{self.dir_relpath / onesrcdir}".'
            )

            anascrfile = AnaDir(
                monorepo   = self.monorepo,
                dirpath    = onesrcpath,
                stepprints = self.stepprints,
                logfile    = self.logfile
            )
         
            self.loginfo(
                message  = f'Working on "{SRC_DIR_NAME}/{onesrcdir}".',
                isitem   = True,
                isnewdir = True
            )

            files = srcdirs(
                anadir = anascrfile,
                kind   = TOC.KIND_FILE
            )
            
            if not anascrfile.success:
                self.success = False

            if files == []:
                self.stepprints[0](f"{MESSAGE_WARNING}: no source found.")

            
            # print(files)
        
        if not self.success:
            return
        exit()

# No problem met, we can build everything.
        if self.success:
            NL()
            self.stepprints[0](MESSAGE_FINAL_PROD + 'building.')






            


# Final build broken!
            if not self.success:
                CLEANNNNNN
###
# prototype::
#     message = ; # See Python typing...
#               ???
#     isitem  = ; # See Python typing...
#               ???
#     isnewdir = ; # See Python typing...
#               ???
###
    def loginfo(
        self,
        message : str,
        isitem  : bool = False,
        isnewdir: bool = False,
    ) -> None:
        if isitem:
            message = self.logger.ITEM + message

            if isnewdir:
                self.logger.logfile_NL()

        else:
            self.logger.logfile_NL()
        
        self.logger.appendtologfile(message)
        self.logger.logfile_NL()