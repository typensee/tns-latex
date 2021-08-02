#!/usr/bin/env python3

from .search import *
from .toc    import *


# ---------------- #
# -- ??? -- #
# ---------------- #

###
# ???
###

class SearchCodes(SearchDirFile):

###
# prototype::
#     monorepo = ; // See Python typing...  
#                the path of the directory of the monorepo.
#     package  = ; // See Python typing...
#                the path of one package to analyze.
#     speaker  = ; // See Python typing...
#                an instance of ``toolbox.speaker.allinone.Speaker`` 
#                is used to communicate small ¨infos.
#     problems = ; // See Python typing...
#                an instance of ``toolbox.Problems`` that manages 
#                a basic history of the problems found.
###
    def __init__(
        self,
        monorepo: PPath,
        package : PPath,
        speaker : Speaker,
        problems: Problems,
    ) -> None:
        super().__init__(        
            monorepo = monorepo,
            speaker  = speaker,
            problems = problems
        )

        self.package    = package
        self.relpackage = package - self.monorepo

        self.src_dirs: List[PPath] = []
        
        self.sections: List[str] = ['']*NB_LATEX_SECTIONS

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
    def extract(self) -> None:
        self.recipe(
        # FORALL, CONTEXT_NORMAL,  # Default setting!
            NL,
            {VAR_STEP_INFO: f'Working inside "{self.relpackage}".'}
        )

# Let's go!
        for methodname in [
            "find_srcdirs",
        ]:
            getattr(self, methodname)()

            if not self.success:
                return


###
# ???
###
    def find_srcdirs(self) -> None:
        self.recipe(
        # FORALL, CONTEXT_NORMAL,  # Default setting!
            FORTERM,
                {VAR_STEP_INFO: 'Searching for sources...',
                VAR_LEVEL    : 1},
        )

# Automatic search of directories.
        if not self.from_about() and self.success:
            self.from_auto()

# No source directory found!
        if not self.src_dirs:
            self.new_critical(
                src_relpath = self.package,
                info        = 'No source directory found!',
                level       = 2 
            )
            return

# Let's talk to the world...
        nb_srcdirs = len(self.src_dirs)
        plurial    = "y" if nb_srcdirs == 1 else "ies"

        self.recipe(
        # FORALL, CONTEXT_NORMAL,  # Default setting!
            FORTERM,
                {VAR_STEP_INFO: f'{nb_srcdirs} source directo{plurial} found.',
                 VAR_LEVEL    : 1},
        )

        print(self.src_dirs)


###
# ???
###
    def from_about(self) -> bool:
# No about file.
        if not self.has_about(self.package):
            return False

# An about file.
        self.recipe(
        # FORALL, CONTEXT_NORMAL,  # Default setting!
            FORTERM,
                {VAR_STEP_INFO: 'One about file found. Looking for metainfos.',
                 VAR_LEVEL    : 1},
            FORLOG,
                {VAR_STEP_INFO: 'One about file found.',
                 VAR_LEVEL    : 1},
        )

        infos = self.about_content()

# Bad formatted about file!
        if not self.success:
            return 

# No TOC inside the about file.
        if not TOC_TAG in infos:
            self.recipe(
            # FORALL, CONTEXT_NORMAL,  # Default setting!
                {VAR_STEP_INFO: 'No TOC inside the about file.',
                 VAR_LEVEL    : 1},
            )

            return False

# One TOC inside the about file.
        self.recipe(
        # FORALL, CONTEXT_NORMAL,  # Default setting!
            FORTERM,
                {VAR_STEP_INFO: 'Using TOC from the about file...',
                 VAR_LEVEL    : 1},
        )

        TODO

        toc = TOC(
            anadir = anadir,
            kind   = kind
        )

        paths = toc.build()

        if kind == toc.kind:
            anadir.problems.new_error(
                src_relpath = anadir.dir_relpath,
                message     = f'"{kind}" expected in TOC but "{toc.kind}" found'
            ) 

        if not anadir.success:
            return

        methodused = f"TOC in ``{anadir.dir_relpath / ABOUT_NAME}``"



###
# ???
###
    def from_auto(self) -> None:
        self.recipe(
        # FORALL, CONTEXT_NORMAL,  # Default setting!
            FORTERM,
                {VAR_STEP_INFO: 'Automatic search of source directories...',
                 VAR_LEVEL    : 1},
            FORLOG,
                {VAR_STEP_INFO: 'Automatic search of source directories.',
                 VAR_LEVEL    : 1},
        )

        for subdir in self.package.iterdir():
# Something to analyze directly in our folder?
            relpath = subdir - self.package
            
            if (
                relpath.depth == 0 
                and
                self.is_kept(
                    onepath = subdir,
                    kind    = DIR_TAG
                )
            ):
                self.src_dirs.append(subdir)
                
        self.src_dirs.sort()
