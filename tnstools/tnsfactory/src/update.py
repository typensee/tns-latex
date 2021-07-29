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
#     srcpaths = ( [] ); // See Python typing...  
#                a list of the source paths to analyze. This argument  
#                can be used when calling Update after another process 
#                has already found the sources to analyze.
###
    def __init__(
        self,
        monorepo: PPath,
        initrepo: bool,
        style   : str,
        srcpaths: List[PPath] = [],
    ) -> None:
        self.srcpaths = srcpaths
        self.initrepo = initrepo
        self.monorepo = monorepo

        self.rel_monorepo = PPath(monorepo.name)

        self.speaker  = Speaker(
            logfile = monorepo / f"x-{monorepo.name}-x.log",
            style   = style
        )

        self.problems = Problems(self.speaker)
        self.success  = None

###
# prototype::
#     see = speaker.allinone.Speaker.recipe
# 
# This method is just an esay-to-use wrapper.
###
    def recipe(self, *args, **kwargs) -> None:
        self.speaker.recipe(*args, **kwargs)

###
# prototype::
#     see = problems.Problems.new_error
# 
# This method is just an esay-to-use wrapper.
###
    def new_error(self, *args, **kwargs):
        self.success = False
        self.problems.new_error(*args, **kwargs)

###
# prototype::
#     see = problems.Problems.new_warning
# 
# This method is just an esay-to-use wrapper.
###
    def new_warning(self, *args, **kwargs):
        self.problems.new_warning(*args, **kwargs)

###
# prototype::
#     see = problems.Problems.resume
# 
# This method is just an esay-to-use wrapper.
###
    def resume(self, *args, **kwargs):
        self.problems.resume(*args, **kwargs)


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
            "find_srcpaths",
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
        self.recipe(
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
                {VAR_TITLE:
                    f'LOG FILE - TNS LIKE MONOREPO "{self.monorepo.name}"'},
            #
            FORALL,
                CONTEXT_NORMAL,
# Title for the start.
            #
            FORTERM,
                {VAR_TITLE: "STARTING THE ANALYSIS", 
                 VAR_LEVEL: 2},
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
        self.resume()

# Just say "Good bye!"
        self.recipe(
            #
            FORALL,
                NL,
# Title for the end.
            #
            FORTERM,
                {VAR_TITLE: "ANALYSIS FINISHED", 
                 VAR_LEVEL: 2},
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
    def find_srcpaths(self):
# Source already found.
        if self.srcpaths:
            return

# We have to look for sources to analyze.
        actiontodo = "create" if self.initrepo else "update"
        allornot   = "all "   if self.initrepo else ""

        self.recipe(
            FORALL,
                {VAR_STEP_INFO: (
                    f'Looking for {allornot}packages to {actiontodo} '
                    f'(initrepo = {self.initrepo}).')},
        )

        actiontodo = actiontodo.replace("te", "ted")

# No source found.
        if not self.srcpaths:
            self.success = False

            for _ in range(25):
                self.new_warning(
                    src_relpath = self.rel_monorepo / "2",
                    info        = f'no packages found to be {actiontodo}.',
                )
                self.new_warning(
                    src_relpath = self.rel_monorepo / "12",
                    info        = f'no packages found to be {actiontodo}.',
                )

                self.new_error(
                    src_relpath = self.rel_monorepo / "004",
                    info        = f'no packages found to be {actiontodo}.',
                )

                self.new_error(
                    src_relpath = self.rel_monorepo / "2",
                    info        = f'no packages found to be {actiontodo}.',
                )

            return
        


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
