#! /usr/bin/env python3

from .about       import *
from .common      import *
from .logit       import *
from .problems    import *
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
#     stepprints = ; # See Python typing...
#                  the functions used to print ¨infos in the terminal.
#     logfile    = ; # See Python typing...
#                  the path of the log file.
###
    def __init__(
        self,
        monorepo  : PPath,
        dirpath   : PPath,
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

        self.final_blocks = {
            ext: {
                t: []
                for t in titles
                if t != TEX_END_DOC
            }
            for ext, titles in FILE_BLOCK.items()
        }

        self.final_blocks[TEX_FILE_EXT][LATEX_TECH_SIGN_TITLE] = []

        for ext in FILE_BLOCK:
            self.final_blocks[ext][EXTRA_RESOURCES] = []

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


#         OKKKK

# # No problem met, we can build everything.
#         NL()
#         self.terminfo(MESSAGE_FINAL_PROD + 'building.')       

# # Final build broken!
#         if not self.success:
#             CLEANNNNNN





###
# This method tries to analyze the ``about.peuf`` file of the package.
###
    def build_about(self) -> None:
        self.terminfo(MESSAGE_ABOUT + "looking for metainfos.")

        self.loginfo(f'{MESSAGE_WORKING} inside "{self.dir_relpath}"...')

        self.about = About(self).build()

###
# This method tries to find the folders of the sources of the package.
###
    def build_srcdirs(self) -> None:
        NL()
        self.terminfo(f"{MESSAGE_SRC}: searching...")

        anascrdir = AnaDir(
            monorepo   = self.monorepo,
            dirpath    = self.dirpath / SRC_DIR_NAME,
            stepprints = self.stepprints,
            logfile    = self.logfile
        )
         
        self.srcdirs = srcdirs(
            anadir = anascrdir,
            kind   = TOC.KIND_DIR
        )

        self.success = anascrdir.success

###
# This method analyzes the sources of the package and prepares the building
# of the final sources. See ``self.finalprod.anafiles(files)``.
###
    def analyze_srcdirs(self) -> None:
        for onesrcdir in self.srcdirs:
            onesrcpath     = self.dirpath     / SRC_DIR_NAME / onesrcdir
            onesrc_relpath = onesrcpath - self.monorepo

            NL()

# Does the dir exist?
            if not onesrcpath.is_dir():
                self.problems.new_error(
                    src_relpath = onesrc_relpath,
                    message     = f'missing dir "{onesrc_relpath}"'
                )
               
                continue

# The dir exists.
            self.terminfo(
                f'{MESSAGE_SRC}: analyzing "{onesrc_relpath}".'
            )

            anascrfile = AnaDir(
                monorepo   = self.monorepo,
                dirpath    = onesrcpath,
                stepprints = self.stepprints,
                logfile    = self.logfile
            )
         
            self.loginfo(
                message  = f'{MESSAGE_WORKING} inside "{onesrc_relpath}".',
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
                self.problems.new_warning(
                    src_relpath = onesrc_relpath,
                    message     = "no source found."
                )
                
                continue

# Let's update the final product.
            self.terminfo(
                f'{MESSAGE_FINAL_PROD}: building some parts...'
            )

            self.finalprod.anafiles(
                packpath = self.dirpath,
                files    = files
            )

        from pprint import pprint;
        print(EXTRA_RESOURCES)
        pprint(self.final_blocks[TEX_FILE_EXT][EXTRA_RESOURCES])
        exit()
