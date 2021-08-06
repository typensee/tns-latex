#! /usr/bin/env python3

from toolbox import *

# crérer pacj utilitaire latex : qui par exemple permet d'avoitr les fichiers utilisés par un doc pour la compile : on commence ç casser misstol




# ------------- #
# -- UPDATER -- #
# ------------- #


###
# This class manages the different processes need to find any LaTeX 
# monorepo respecting the ¨tns way of coding.
###

###
# This class manages the different processes need to find all the source codes
# of a monorepo respecting the ¨tns way of coding.
###

class Update(BaseCom):
###
# prototype::
#     monorepo = ; // See Python typing...  
#                the path of the directory of the monorepo.
#     initrepo = ; // See Python typing...  
#                ``True`` forces to work on all packages without using
#                term::``git a`` and False uses git to focus only on
#                recent changes.
#     problems = ; // See Python typing...  
#                an instance of ``toolbox.Problems`` that manages 
#                a basic history of the problems found.
#
# info::
#     The sources found will be stored in the dict ``self.src_found`` that 
#     will look like this:
#
#     python::
#         {
#             "name of a package": {
#                 "one source subdir": [
#                     "list", "of", "source", "files"
#                 ]
#             }
#         }
###
    def __init__(
        self,
        monorepo: PPath,
        initrepo: bool,
        problems: Problems,
    ) -> None:
        super().__init__(
            monorepo    = monorepo,
            problems    = problems
        )

        self.initrepo = initrepo

        self.src_found: dict = {}


###
# Here is the great bandleader.
###
    def build(self) -> None:
# Let's be optimistic...
        self.success = True

# Let's work.
        for methodname in [
            "open_session",
            "find_sources",
            "close_session",
        ]:
            getattr(self, methodname)()

            if not self.success:
                break


###
# prototype::
#     :see: = findall_sources.FindAllSources
#
# This method builds ``self.src_found`` which is a dict looking like this:
#
# python::
#     {
#         "name of a package": {
#             "1st source subdir": [
#                 "list", "of", "source", "files"
#             ],
#             "2nd source subdir": [
#                 "another", "list", "of", "sources"
#             ],
#         }
#     }
###
    def find_sources(self) -> None:
        findall = FindAllSources(
            monorepo = self.monorepo,
            initrepo = self.initrepo,
            problems = self.problems
        )

        findall.build()

        if not findall.success:
            self.success = findall.success
            return

        self.src_found = findall.src_found


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

    updater = Update(
        monorepo = MONOREPO,
        initrepo = INIT_REPO,
        problems = problems
    )

    updater.build()

    for k, v in updater.src_found.items():
            k = k.name

            print('---')
            print(k)

            for kk, vv in v.items():
                kk = kk.name

                vv = [x.name for x in vv]

                print(kk)
                print(vv)
                print()

