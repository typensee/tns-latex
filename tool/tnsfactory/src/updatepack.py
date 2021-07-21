#! /usr/bin/env python3

from .about       import *
from .common      import *
from .logit       import *
from .finalprod   import *
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
        assert kind in TOC.ALL_USER_KINDS, \
               f'kind = "{kind}" for TOC not in {self.ALL_USER_KINDS}.'

        super().__init__(
            monorepo   = monorepo,
            dirpath    = dirpath,
            stepprints = stepprints,
            logfile    = logfile,
            needabout  = True
        )

        self.kind      = kind
        self.finalprod = FinalProd(
            anadir = self,
            kind   = kind
        )

###
# Here is the great bandleader.
###
    def build(self) -> None:
# Let's be optimism.
        self.success = True

# Let's go!
        for methodname in [
            "build_about",
            "build_srcdirs",
            "analyze_srcdirs",
        ]:
            getattr(self, methodname)()

            if not self.success:
                return


        OKKKK

# No problem met, we can build everything.
        NL()
        self.stepprints[0](MESSAGE_FINAL_PROD + 'building.')






            


# Final build broken!
        if not self.success:
            CLEANNNNNN





###
# This method tries to analyze the ``about.peuf`` file of the package.
###
    def build_about(self) -> None:
        self.stepprints[0](MESSAGE_ABOUT + "looking for metainfos.")

        self.loginfo(f'Working on "{self.dir_relpath}"...')

        self.about = About(self).build()

###
# This method tries to find the folders of the sources of the package.
###
    def build_srcdirs(self) -> None:
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

###
# This method analyzes the sources of the package.
###
    def analyze_srcdirs(self) -> None:
        for onesrcdir in self.srcdirs:
            onesrcpath     = self.dirpath     / SRC_DIR_NAME / onesrcdir
            onesrc_relpath = onesrcpath - self.monorepo

            NL()

# Does the dir exist?
            if not onesrcpath.is_dir():
                message = f'missing dir "{onesrc_relpath}"'

                self.stepprints[0](f'{MESSAGE_PROBLEM}: {message}.')
                self.error(message)
                
                continue

# The dir exists.
            self.stepprints[0](
                MESSAGE_SRC 
                +
                f'analyzing "{onesrc_relpath}".'
            )

            anascrfile = AnaDir(
                monorepo   = self.monorepo,
                dirpath    = onesrcpath,
                stepprints = self.stepprints,
                logfile    = self.logfile
            )
         
            self.loginfo(
                message  = f'Working on "{onesrc_relpath}".',
                isitem   = True,
                isnewdir = True
            )

            files = srcdirs(
                anadir = anascrfile,
                kind   = TOC.KIND_FILE
            )
            
            if not anascrfile.success:
                self.success = False

# No file found.
            if files == []:
                message = "no source found."
                
                self.warning(message)
                self.stepprints[0](f"{MESSAGE_WARNING}: {message}")
                continue

# Let's update the final product.
            self.finalprod.addfiles(files)











###
# prototype::
#     message = ; # See Python typing...
#               the message to append to the log file.
#     isitem  = ; # See Python typing...
#               ``True`` indicates to print an item and
#               ``False`` to no do that. 
#     isnewdir = ; # See Python typing...
#               ``True`` when starting to work on an new
#               folder and ``False`` in other cases.
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
