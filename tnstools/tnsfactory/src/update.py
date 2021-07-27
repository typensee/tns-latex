#! /usr/bin/env python3

from tools import *


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
###
    def __init__(
        self,
        monorepo: PPath,
        initrepo: bool
    ) -> None:

        self.monorepo = monorepo

        self.speaker  = Speaker(
            logfile = monorepo / "x-LOG-LATEX-MONOREPO-x.txt",
            # stylist = ColorStylist
            stylist = BWStylist
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
        self.speaker.receipe(
# Title for the monorepo.
            (SPK_STYLE, SPK_STYLE_GOOD),
            SPK_FORTERM,
            SPK_NL,
            (SPK_TITLE, f'TNS LIKE MONOREPO "{self.monorepo.name}"'),
            #
            SPK_FORLOG,
            (SPK_TITLE, f'LOG FILE - TNS LIKE MONOREPO "{self.monorepo.name}"'),
            #
            SPK_FORALL,
            SPK_STYLE,
# Title for the start.
            SPK_FORTERM,
            (SPK_TITLE, {SPK_VAR_TITLE: "STARTING THE ANALYSIS", 
                         SPK_VAR_LEVEL: 2}),
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
        self.speaker.receipe(
# Terminal output.
            SPK_FORTERM,
            SPK_NL,
            (SPK_TITLE, {SPK_VAR_TITLE: "ANALYSIS FINISHED", 
                         SPK_VAR_LEVEL: 2}),
# Log file output.
            SPK_FORLOG,
            SPK_NL
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
        self.speaker.receipe(
# Terminal output.
            SPK_FORTERM,
            (SPK_STEP, "Looking for packages to build or update."),
        )

        self.speaker.receipe(
# Terminal output.
            SPK_FORALL,
            (SPK_STYLE, SPK_STYLE_ERROR),
            SPK_NL,
            (SPK_PROBLEM, {SPK_VAR_MESSAGE: "No packages found.",
                           SPK_VAR_CONTEXT: "ERROR", 
                           SPK_VAR_PB_ID  : 0}),
            SPK_STYLE,
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
        initrepo = INIT_REPO
    )
    update.build()
