#! /usr/bin/env python3

from toolbox import *


# ---------------- #
# -- MAIN CLASS -- #
# ---------------- #

###
# This class manages the different processes need to work update 
# any LaTeX monorepo respecting the ¨tns way of coding.
###
class Update:
###
# prototype::
#     monorepo = ; // See Python typing...  
#               the path of the directory of the monorepo.
#     initrepo = ; // See Python typing...  
#               ``True`` forces to work on all packages without using
#               term::``git a`` and False uses git to focus only on
#               recent changes.
#     style    = _ in interface.GLOBAL_STYLES; // See Python typing...  
#                a global style for the output.
###
    def __init__(
        self,
        monorepo: PPath,
        initrepo: bool,
        style   : str 
    ) -> None:
        self.monorepo = monorepo

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

        for methodname in [
            "findpacks",
        ]:
            getattr(self, methodname)()

            if not self.success:
                self.close_session()
                return

# Everything seems ok...
        self.close_session()


###
# This method indicates the begin of the work.
###
    def open_session(self):
# Just say "Hello."
        self.speaker.recipe(
# Title for the monorepo.
            CONTEXT_GOOD,
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
            FORTERM,
            {VAR_TITLE: "STARTING THE ANALYSIS", 
             VAR_LEVEL: 2},
        )

        timestamp(
            speaker = self.speaker,
            kind    = "STARTING"
        )


###
# This method first cleans the monorepo and then indicates the end 
# of the process.
###
    def close_session(self):
# TODO résumé ici !!!

# Just say "Good bye!"
        self.speaker.recipe(
# Terminal output.
            FORTERM,
            NL,
            {VAR_TITLE: "ANALYSIS FINISHED", 
             VAR_LEVEL: 2},
# Log file output.
            FORLOG,
            NL
        )

        timestamp(
            speaker = self.speaker,
            kind    = "ENDING"
        )
        self.speaker.forall()


###
# This method looks for packages to work on.
###
    def findpacks(self):
        self.speaker.recipe(
# Terminal output.
            FORTERM,
            {VAR_STEP_INFO: "Looking for packages to build or update."},
        )

        self.speaker.recipe(
# Terminal output.
            FORALL,
            NL,
            {VAR_CONTEXT: CONTEXT_ERROR,
             VAR_INFO: "No packages found.",
             VAR_PB_ID  : 0},
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
        NOT_IMPLEMENTED

    update = Update(
        monorepo = MONOREPO,
        initrepo = INIT_REPO,
        style    = GLOBAL_STYLE_COLOR,
        # style    = GLOBAL_STYLE_BW
    )
    update.build()
