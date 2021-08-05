#!/usr/bin/env python3

from mistool.string_use import joinand

from orpyste.data      import ReadBlock
from orpyste.parse.ast import ASTError

from ..base import *

from .config import *
from .toc import *
from ..problems import *


# ----------------------------------------------- #
# -- BASE CLASS FOR GOOD FILES AND DIRECTORIES -- #
# ----------------------------------------------- #

###
# This class proposes methods to search ¨tnslatex like packages and 
# files to analyze.
###

class SearchDirFile(BaseCom):

###
# prototype::
#     monorepo = ; // See Python typing...  
#                the path of the directory of the monorepo.
#     problems = ; // See Python typing...  
#                an instance of ``toolbox.Problems`` that manages 
#                a basic history of the problems found.
###
    def __init__(
        self,
        monorepo: PPath,
        problems: Problems,
    ) -> None:
        super().__init__(
            monorepo = monorepo,
            problems = problems,
        )

        self.last_about = None


###
# prototype::
#     source = ; // See Python typing...
#              the path of a source.
#     kind   = _ in [DIR_TAG, FILE_TAG] ; // See Python typing...
#              the kind of source.
#
#     :return: = ; // See Python typing...
#                ``True`` if the source physically exists and
#                ``False`` otherwise.
###
    def exists(
        self, 
        source: PPath,
        kind  : str,
    ) -> bool:
        if kind == DIR_TAG:
            return source.is_dir()

        return source.is_file()


###
# prototype::
#     onedir      = ; // See Python typing...  
#                   the path of a directory .
#     kind        = _ in [DIR_TAG, FILE_TAG]; // See Python typing...
#                   the kind of ¨io objects wanted.
#     main_reldir = ; // See Python typing...
#                   a path of a containing directory.
#
#     :return: = ; // See Python typing...
#                this method iterates unrecursively inside the content of
#                a directory and yields the ¨io objects found that are not
#                ignored regarding the specifications of the ¨tnslatex 
#                like packages.
#
#     :see: = self.is_kept
###
    def iterIOkept(
        self, 
        onedir     : PPath, 
        kind       : str,
        main_reldir: PPath,
    ) -> Iterator[PPath]:
        for fileordir in onedir.iterdir():
            if self.is_kept(
                onepath     = fileordir,
                kind        = kind,
                main_reldir = main_reldir
            ):
                yield fileordir

###
# prototype::
#     onepath     = ; // See Python typing...
#                   a path of a file or a directory.
#     kind        = _ in [DIR_TAG, FILE_TAG]; // See Python typing...
#                   the kind of infos wanted.
#     main_reldir = ; // See Python typing...
#                   a path of a containing directory.
#
#     :return: = ; // See Python typing...
#                ``True`` for a file or a directory to keep and
#                ``False`` in the opposite case.
###
    def is_kept(
        self,
        onepath    : PPath,
        kind       : str,
        main_reldir: PPath,
    ) -> bool:
# Good kind?
        if kind == DIR_TAG:
            if not onepath.is_dir():
                return False

        else:
            if not onepath.is_file():
                return False

# Something to ignore?
        if any(
            not p.match(onepath.stem) is None
            for p in PATTERNS_SPECIAL[kind]
        ):
            return False

# Nothing more to do for folders.
        if kind == DIR_TAG:
            return True

# We keep only files with specific extensions.
        if not onepath.ext in FILE_EXT_WANTED:
            return False

# ¨latex doc must be name like ``mydoc-EN.tex``.
        if onepath.ext == TEX_FILE_EXT:
            if PATTERN_LATEX_DOC.match(onepath.stem) is None:
                self.new_warning(
                    src_relpath = main_reldir,
                    info        = (
                        f'LaTeX file "{onepath.name}" ignored. '
                         '\n'
                        f'You can use a name like "{onepath.stem}-EN.{TEX_FILE_EXT}".'
                         '\n'
                        f'List of languages available: {joinand(ALL_LANGS)}.'
                    ),
                    level = 2
                )

                return False

# No more things to test for a file.
        return True


###
# prototype::
#     onedir = ; // See Python typing...
#              the path of the directory to keep or not.
#
#     :return: = ; // See Python typing...
#                ``True`` for a directory whit  an ``about.peuf`` file, or 
#                ``False`` in other cases.
#
# This method manages the value of the attribut ``self.about``.
#
# warning::
#     If no about file is found, the value of ``self.about`` is ``None``.
###
    def has_about(self, onedir: PPath) -> bool:
        self.last_about = onedir / ABOUT_NAME

        if self.last_about.is_file():
            return True

        self.last_about = None

        return False

###
# prototype::
#     level = _ in [0..3] (0); // See Python typing...
#             the level of step indicating where ``0`` is for automatic 
#             numbered enumerations (this for emitting errors).
#
#     :return: = ; // See Python typing...
#                the "semantic dict" content of the ``about.peuf`` file.
#
# warning:
#     ``self.has_about``  **must be used just before** the call of 
#     this method.
###
    def about_content(self, level: int = 0) -> dict:
        try:
            with ReadBlock(
                content = self.last_about,
                mode    = ABOUT_PEUF_MODE
            ) as datas:
                infos = datas.mydict("std nosep nonb")
    
        except ASTError:
            relpath = self.last_about - self.monorepo

            self.new_error(
                src_relpath = relpath,
                info        = f'about file "{relpath}" bad formatted.',
                level       = level
            )
            return 

        return infos


###
# prototype::
#     onedir   = ; // See Python typing...
#                a directory where to look for sources.
#     attrname = ; // See Python typing...
#                the name of the attribut that will store the list of paths found.
#     kind     = _ in [DIR_TAG, FILE_TAG]; // See Python typing...
#                the kind of sources wanted.
#     level    = _ in [0..3] (0); // See Python typing...
#                the level of step indicating where ``0`` is for automatic 
#                numbered enumerations.
#
# This method is an abstraction to analyze either file sources, or dir. sources.
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
# prototype::
#     onedir   = ; // See Python typing...
#                a directory where to look for sources given in a about file.
#     attrname = ; // See Python typing...
#                the name of the attribut that will store the list of 
#                paths found.
#     kind     = _ in [DIR_TAG, FILE_TAG]; // See Python typing...
#                the kind of sources wanted.
#     level    = _ in [0..3] (0); // See Python typing...
#                the level of step indicating where ``0`` is for automatic 
#                numbered enumerations.
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
        toc = TOC(
            monorepo = self.monorepo,
            onedir   = onedir,
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
            FORTERM,
                {VAR_STEP_INFO: 'Using TOC from the about file...',
                 VAR_LEVEL    : level},
        )

        strpaths = toc.extract()

# Something wrong has happened.
        if not toc.success:
            self.success = toc.success
            return

# We complete the list with LaTeX doc files if they exist.
        paths = self.docassotosty(
            onedir   = onedir,
            strpaths = strpaths
        )

# We store the list of paths found.
        setattr(self, attrname, paths)

# Everything seems ok.
        return True

###
# prototype::
#     onedir   = ; // See Python typing...
#                a directory where to look for ¨latex files associated to 
#                a path::``STY`` file.
#     strpaths = ; // See Python typing...
#                the list of relative path of the source files found by 
#                using the about file.
#
#     :return: = ; // See Python typing...
#                the sorted list of all source files.
###
    def docassotosty(
        self, 
        onedir  : PPath,
        strpaths: List[str]
    ) -> List[PPath]:
        paths: List[PPath] = []

        for onestrpath in strpaths:
            onepath = onedir / onestrpath

            paths.append(onepath)

# No LaTeX doc to search.
            if onepath.ext != STY_FILE_EXT:
                continue

# Let seek and destroy as Metalica used to do.
            sty_name = onepath.stem

            tex_associated = []

            for onefile in onedir.iterdir():
                if (
                    not onefile.is_file()
                    or
                    onefile.ext != TEX_FILE_EXT                        
                ):
                    continue
                
                if (
                    onefile.name.startswith(f'{sty_name}-')
                    or
                    f'-{sty_name}-' in onefile.name
                ):
                    if not PATTERN_LATEX_DOC.match(onefile.stem) is None:
                        tex_associated.append(PPath(onefile))

            if tex_associated:
                tex_associated.sort()

                paths += tex_associated

                nb_texfound = len(tex_associated)
                plurial     = "" if nb_texfound == 1 else "s"

                self.recipe(
                    {VAR_STEP_INFO: (
                        f'{nb_texfound} LaTeX file{plurial} automatically '
                        f'associated to "{onepath.name}".'),
                     VAR_LEVEL: 2},
                )

# Nothing more to do...
        return paths


###
# prototype::
#     onedir   = ; // See Python typing...
#                a directory where to look in for sources automatically.
#     attrname = ; // See Python typing...
#                the name of the attribut that will store the list of 
#                paths found.
#     kind     = _ in [DIR_TAG, FILE_TAG]; // See Python typing...
#                the kind of sources wanted.
#     level    = _ in [0..3] (0); // See Python typing...
#                the level of step indicating where ``0`` is for automatic 
#                numbered enumerations.
###
    def from_auto(
        self, 
        onedir  : PPath,
        attrname: str,
        kind    : str,
        level   : int
    ) -> None:
        self.recipe(
            {VAR_STEP_INFO: f'Automatic search of {kind} sources.',
             VAR_LEVEL    : level},
        )

        paths = []

        for subdir in self.iterIOkept(
            onedir      = onedir,
            kind        = kind,
            main_reldir = self.relpackage
        ):
            paths.append(subdir)

        paths.sort()

        setattr(self, attrname, paths)
