#!/usr/bin/env python3

from .search_base import *
from .toc         import *


# ---------------- #
# -- ??? -- #
# ---------------- #

###
# ???
###

class SearchSources(SearchDirFile):

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
    
        self.src_package            = package / SRC_DIR_NAME
        self.src_relpackage         = self.src_package - self.monorepo
        
        self.src_dirs : List[PPath]       = []
        self.src_files: List[PPath]       = []
        self._temp_src_files: List[PPath] = []

        self._toc_used = False
        
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
            "find_srcfiles",
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

# Build source dirs.
        self.build_sources(
            onedir   = self.src_package,
            attrname = "src_dirs",
            kind     = DIR_TAG,
            level    = 1
        )


###
# This method analyzes the sources of the package and prepares the building
# of the final sources. See ``self.finalprod.anafiles(files)``.
###
    def find_srcfiles(self) -> None:
        self.src_files = []

        for onesrcdir in self.src_dirs:
            onesrcdir_rel = onesrcdir - self.monorepo
            self.recipe(
            # FORALL, CONTEXT_NORMAL,  # Default setting!
                NL,
                {VAR_STEP_INFO: f'Working in "{onesrcdir_rel}".',
                 VAR_LEVEL    : 1},
            )

# Build source files.
            self.build_sources(
                onedir   = onesrcdir,
                attrname = "_temp_src_files",
                kind     = FILE_TAG,
                level    = 2
            )

            if not self.success:
                return
            
            self.src_files += self._temp_src_files


###
# ???
###
    def build_sources(
        self, 
        onedir  : PPath,
        attrname: str,
        kind    : str,
        level   : int
    ) -> None:
        onedir_rel = onedir - self.monorepo

# No main source dir.
        if not onedir.is_dir():
            self.new_critical(
                src_relpath = onedir_rel,
                info        = f'missing dir:\n"{onedir_rel}"',
                level       = level
            )

            return

# A TOC from a about file or an automatic search of directories.
        if self.from_about(
            onedir   = onedir,
            attrname = attrname,
            kind     = kind,
            level    = level
        ):
            self._toc_used = True

        else:
            if not self.success:
                return

            self._toc_used = False

            self.from_auto(
                onedir   = onedir,
                attrname = attrname,
                kind     = kind,
                level    = level
            )

# No source directory found!
        if not getattr(self, attrname):
            self.new_critical(
                src_relpath = onedir_rel,
                info        = f'No source found inside :\n"{onedir_rel}"',
                level       = 2 
            )

# A source found but that is not real.
        for onesrc in getattr(self, attrname):
            if not self.exists(
                source = onesrc,
                kind   = kind
            ):
                onesrc_rel = onesrc - self.monorepo

                self.new_error(
                    src_relpath = onesrc_rel,
                    info        = f'missing {kind} source:\n"{onesrc_rel}"',
                    level       = 2 
                )

                return

# Let's talk to the world...
        nb_sources         = len(getattr(self, attrname))
        plurial            = "" if nb_sources == 1 else "s"
        log_message_method = (
            " (TOC used)"
            if self._toc_used else
            ""
        )

        self.recipe(
        # FORALL, CONTEXT_NORMAL,  # Default setting!
            FORTERM,
                {VAR_STEP_INFO:
                    f'{nb_sources} source {kind}{plurial} found.',
                 VAR_LEVEL: level},
            FORLOG,
                {VAR_STEP_INFO:
                    f'{nb_sources} source {kind}{plurial} found{log_message_method}.',
                 VAR_LEVEL: level},
        )

###
# ???
###
    def exists(
        self, 
        source: PPath,
        kind  : str,
    ):
        if kind == DIR_TAG:
            return source.is_dir()

        return source.is_file()

###
# ???
###
    def from_about(
        self, 
        onedir  : PPath,
        attrname: str,
        kind    : str,
        level   : int
    ) -> bool:
# No about file
        if not self.has_about(onedir):
            return False

# An about file.
        self.recipe(
        # FORALL, CONTEXT_NORMAL,  # Default setting!
            FORTERM,
                {VAR_STEP_INFO: 'One about file found. Looking for metainfos.',
                 VAR_LEVEL    : level},
            FORLOG,
                {VAR_STEP_INFO: 'One about file found.',
                 VAR_LEVEL    : level},
        )

        infos = self.about_content(level = level)

# Bad formatted about file!
        if not self.success:
            return 

# Try to work with a TOC.
# TODO une seule instance que l'on reset !!!
        toc = TOC(
            monorepo = self.monorepo,
            onedir   = onedir,
            speaker  = self.speaker ,
            problems = self.problems,
            infos    = infos,
            kind     = kind,
            level    = level + 1
        )

# No TOC inside the about file.
        if not toc.has_toc():
            self.new_warning(
                src_relpath = self.relpackage,
                info        = 'no TOC inside the about file.',
                level       = level
            )

            return False

# One TOC inside the about file.
        self.recipe(
        # FORALL, CONTEXT_NORMAL,  # Default setting!
            FORTERM,
                {VAR_STEP_INFO: 'Using TOC from the about file...',
                 VAR_LEVEL    : level},
        )

        strpaths = toc.extract()

# Something wrong has happened.
        if not toc.success:
            self.success = toc.success
            return 

# ???
        paths = [
            onedir / p
            for p in strpaths
        ]
        
        setattr(self, attrname, paths)

# Everything seems ok.
        return True

###
# ???
###
    def from_auto(
        self, 
        onedir  : PPath,
        attrname: str,
        kind    : str,
        level   : int
    ) -> None:
        self.recipe(
        # FORALL, CONTEXT_NORMAL,  # Default setting!
            {VAR_STEP_INFO: f'Automatic search of {kind} sources.',
             VAR_LEVEL    : level},
        )

        paths = []

        for subdir in self.iterIO(
            onedir = onedir,
            kind   = kind
        ):
            paths.append(subdir)

        paths.sort()

        setattr(self, attrname, paths)
