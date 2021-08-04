#! /usr/bin/env python3

from toolbox import *


# ------------- #
# -- UPDATER -- #
# ------------- #

###
# This class manages the different processes need to update any LaTeX 
# monorepo respecting the ¨tns way of coding.
###

class Update(SearchPacks):
###
# prototype::
#     monorepo    = ; // See Python typing...  
#                   the path of the directory of the monorepo.
#     initrepo    = ; // See Python typing...  
#                   ``True`` forces to work on all packages without using
#                   term::``git a`` and False uses git to focus only on
#                   recent changes.
#     problems    = ; // See Python typing...  
#                   an instance of ``toolbox.Problems`` that manages 
#                   a basic history of the problems found.
#     packs_paths = ( [] ); // See Python typing...  
#                   a list of the source paths to analyze. This argument 
#                   can be used when calling ``Update`` after another 
#                   process has already found the sources to analyze.
###
    def __init__(
        self,
        monorepo   : PPath,
        initrepo   : bool,
        problems   : Problems,
        packs_paths: List[PPath] = [],
    ) -> None:
        super().__init__(
            monorepo    = monorepo,
            initrepo    = initrepo,
            problems    = problems,
            packs_paths = packs_paths
        )


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
            "search_packs" , # See ``filendir.search_packs.SearchPacks``.
            "analyze_packs",
        ]:
            getattr(self, methodname)()

            if not self.success:
                break

# We must close and clean the dirty things.
        self.close_session()


###
# This method indicates the begin of the work.
###
    def open_session(self) -> None:
# Just say "Hello."
        self.recipe(
                CONTEXT_GOOD,
            #
            FORTERM,
                NL,
                {VAR_TITLE: f'TNS LIKE MONOREPO "{self.monorepo.name}"'},
            #
            FORLOG,
                {VAR_TITLE:
                    f'LOG FILE - TNS LIKE MONOREPO "{self.monorepo.name}"'},
        )

        self.recipe(
        # Title for the start.
            FORTERM,
                {VAR_TITLE: "STARTING THE ANALYSIS", 
                 VAR_LEVEL: 2},
        )

# A time stamp.
        timestamp(
            speaker = self.problems.speaker,
            kind    = "STARTING"
        )

###
# This method first cleans the monorepo and then indicates the end 
# of the process.
###
    def close_session(self) -> None:
# TODO clean !!!!

# Summary of the problems met.
        self.resume()

# Just say "Good bye!"
        self.recipe(
                NL,
        # Title for the end.
            FORTERM,
                {VAR_TITLE: "ANALYSIS FINISHED", 
                 VAR_LEVEL: 2},
        )

# A time stamp.
        timestamp(
            speaker = self.problems.speaker,
            kind    = "ENDING",
            with_NL = False
        )

###
# ???
###
    def analyze_packs(self) -> None:
 # TODO: manage_resources
        for onepack in self.packs_paths:
            searchcodes = SearchSources(
                monorepo = self.monorepo,
                package  = onepack,
                problems = self.problems
            )

            searchcodes.extract()

            for p in searchcodes.src_files:
                print(p.name)


# ---------- #
# -- TEST -- #
# ---------- #

if __name__ == "__main__":
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



#     style    = _ in speaker.spk_interface.ALL_GLOBAL_STYLES; 
#                a global style for the output.     
    speaker = Speaker(
        logfile = MONOREPO / f"{MONOREPO.name}.tns.log",
        style   = GLOBAL_STYLE_COLOR,
        # style   = GLOBAL_STYLE_BW
    )
    
    problems = Problems(speaker)

    update = Update(
        monorepo = MONOREPO,
        initrepo = INIT_REPO,
        problems = problems
    )

    update.build()
