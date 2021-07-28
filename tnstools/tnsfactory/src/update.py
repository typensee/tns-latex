#! /usr/bin/env python3

from toolbox import *


# ------------- #
# -- UPDATER -- #
# ------------- #

###
# This class manages the different processes need to update 
# any LaTeX monorepo respecting the ¨tns way of coding.
###

class Update:
###
# prototype::
#     monorepo = ; // See Python typing...  
#               the path of the directory of the monorepo.
#     initrepo = ; // See Python typing...  
#                ``True`` forces to work on all packages without using
#                term::``git a`` and False uses git to focus only on
#                recent changes.
#     style    = _ in speaker.spk_interface.ALL_GLOBAL_STYLES; 
#                a global style for the output.
###
    def __init__(
        self,
        monorepo: PPath,
        initrepo: bool,
        style   : str 
    ) -> None:
        self.monorepo = monorepo
        self.initrepo = initrepo

        self.speaker  = Speaker(
            logfile = monorepo / f"x-{monorepo.name}-x.log",
            style   = style
        )

        self.problems = Problems(self.speaker)
        self.success  = None


###
# Here is the great bandleader.
###
    def build(self) -> None:
# Let's be optimistic...
        self.success = True

# Let's go!
        self.open_session()

# Let's work.
        for methodname in [
            "findpacks",
        ]:
            getattr(self, methodname)()

            if not self.success:
                break

# We must close and clean the dirty things.
        self.close_session()


###
# This method indicates the begin of the work.
###
    def open_session(self):
# Just say "Hello."
        self.speaker.recipe(
# Title for the monorepo.
            #
            #FORALL,  # Defaul setting!
                CONTEXT_GOOD,
            #
            FORTERM,
                NL,
                {VAR_TITLE: f'TNS LIKE MONOREPO "{self.monorepo.name}"'},
            #
            FORLOG,
                {VAR_TITLE: f'LOG FILE - TNS LIKE MONOREPO "{self.monorepo.name}"'},
            #
            FORALL,
                CONTEXT_NORMAL,
# Title for the start.
            #
            FORTERM,
                {VAR_TITLE: "STARTING THE ANALYSIS", VAR_LEVEL: 2},
        )

# A time stamp.
        timestamp(
            speaker = self.speaker,
            kind    = "STARTING"
        )

###
# This method first cleans the monorepo and then indicates the end 
# of the process.
###
    def close_session(self):
# TODO clean !!!!

# Summary of the problems met.
        self.problems.resume()

# Just say "Good bye!"
        self.speaker.recipe(
            #
            FORALL,
                NL,
# Title for the end.
            #
            FORTERM,
                {VAR_TITLE: "ANALYSIS FINISHED", VAR_LEVEL: 2},
        )

# A time stamp.
        timestamp(
            speaker = self.speaker,
            kind    = "ENDING",
            with_NL = False
        )


###
# This method looks for packages that will be analyzed.
###
    def findpacks(self):
        action = "" if self.initrepo else " or update"

        self.speaker.recipe(
# Terminal output.
            #
            FORALL,
                {VAR_STEP_INFO: f'Looking for packages to create{action}.'},
                NL,
        )

# No package to update.
        self.problems.new_warning(
            src_relpath = self.monorepo,
            info        = f'no packages to create{action} found.',
        )
        


# ---------- #
# -- TEST -- #
# ---------- #

if __name__ =="__main__":
    INIT_REPO = True
    # INIT_REPO = False

    LANGS_SUPPORTED = ["FR"]

    if "typensee-latex" in __file__:
        MONOREPO = PPath(__file__)

        while(not MONOREPO.name.startswith("typensee-latex")):
            MONOREPO = MONOREPO.parent

    else:
        raise Exception(
            "call the script from a working directory containing the monorepo."
        )

    update = Update(
        monorepo = MONOREPO,
        initrepo = INIT_REPO,
        style    = GLOBAL_STYLE_COLOR,
        # style    = GLOBAL_STYLE_BW
    )
    update.build()
