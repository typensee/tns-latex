#!/usr/bin/env python3

import re

from mistool.os_use import PPath

from .toc import *
from ..problems import *


# ---------------- #
# -- ??? -- #
# ---------------- #



ABOUT_NAME   =  "about.peuf"
SRC_DIR_NAME =  "src"

TOC_TAG  = "toc"
GENE_TAG = "general"

ABOUT_PEUF_MODE = {
    "keyval:: =": GENE_TAG,
    "verbatim"  : TOC_TAG,
}

GENE_TNSLATEX_TAG = "tnslatex"
GENE_DESC_TAG     = "desc"
GENE_AUTHOR_TAG   = "author"
GENE_LICENCE_TAG  = "licence"
GENE_NEED_TAG     = "need"

GENE_ALL_TAGS = set([
    GENE_TNSLATEX_TAG,
    GENE_DESC_TAG    ,
    GENE_AUTHOR_TAG  ,
    GENE_LICENCE_TAG ,
    GENE_NEED_TAG    ,
])

YES_TAG = "yes"
NO_TAG  = "no"




PATTERN_COMMON = [
    "\\..+",
    "x-.+-x",
]

PATTERNS_SPECIAL = {
    DIR_TAG: [
        re.compile(f"^{p}$")
        for p in PATTERN_COMMON + [
            "changes", 
            "tools", 
            "tests"
        ]
    ],
    FILE_TAG: [
        re.compile(f"^{p}$")
        for p in PATTERN_COMMON + [
            "tools?-.*", 
            "tests?-.*"
        ]
    ]
}

###
# ???
###

class SearchPack:

###
# prototype::
#     monorepo    = ; // See Python typing...  
#                   the path of the directory of the monorepo.
#     initrepo    = ; // See Python typing...  
#                   ``True`` forces to work on all packages without using
#                   term::``git a`` and False uses git to focus only on
#                   recent changes.
#     speaker     = ; // See Python typing...  
#                   an instance of ``toolbox.speaker.allinone.Speaker`` 
#                   is used to communicate small ¨infos.
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
        speaker    : Speaker,
        problems   : Problems,
        packs_paths: List[PPath] = [],
    ) -> None:
        self.packs_paths = packs_paths

        self.initrepo         = initrepo
        self.monorepo         = monorepo
        self.monorepo_relpath = PPath(monorepo.name)

        self.speaker  = speaker
        self.problems = problems
        self.success  = None


###
# ???
###
    def search(self) -> None:
# Sources have already been found.
        if self.packs_paths:
            return

        self.packs_paths = []

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

# Let's work.
        self.packs_paths = self.recbuild_paths(self.monorepo)

# No source found.
        if not self.packs_paths:
            self.success = False

            self.new_warning(
                src_relpath = self.monorepo_relpath,
                info        = f'no package found to be {actiontodo}.',
            )

            return

# Sources have been found.
        print(self.packs_paths)





###
# prototype::
#     onedir = ; // See Python typing...
#              the path of the directory of the onedir to explore.
#
#     return = ; // See Python typing...
#              the list of the ``PPath`` of the ¨tnslatex packages.
###
    def recbuild_paths(self, onedir) -> List[PPath]:
        packsfound: List[PPath] = []

        for subdir in onedir.iterdir():
# A folder to analyze.
            if subdir.is_dir() and self.keepthis(subdir, TOC.KIND_DIR):
                if self.istnspack(subdir):
                    packsfound.append(subdir)

                else:
                    packsfound += self.recbuild_paths(subdir)

# Sort the result and return it.
        packsfound.sort()

        return packsfound


###
# prototype::
#     onepath = ; // See Python typing...
#               a path of a file or a directory.
#     kind    = _ in [DIR_TAG, FILE_TAG]; // See Python typing...
#               the kind of infos wanted.
#
#     return  = ; // See Python typing...
#               ``True`` for a file or a directory to keep and
#               ``False`` in the opposite case.
###
    def keepthis(
        self,
        onepath: PPath,
        kind   : bool
    ) -> bool:
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
        return onepath.ext in FILE_EXT_WANTED




###
# prototype::
#     dirpath = ; // See Python typing...
#               the path of the directory to keep or not.
#
#     return = ; // See Python typing...
#              ``True`` for a directory is a tnslatex, or 
#              ``False`` in other cases.
###

    def istnspack(self, dirpath: PPath) -> bool:
        aboutpath = dirpath / "about.peuf"

        return aboutpath.is_file() and self.keepthisabout(aboutpath)


###
# prototype::
#     aboutfile = ; // See Python typing...
#                 the path of an ``about.peuf`` file.
#
#     return = ; // See Python typing...
#              ``True`` if the ``about.peuf`` indicates a ¨tnslatex package, or 
#              ``False`` in other cases.
#
# warning::
#     Errors ares raised if the path::``PEUF`` file is bad formatted.
###

    def keepthisabout(self, aboutfile: PPath) -> bool:
        with ReadBlock(
            content = aboutfile,
            mode    = ABOUT_PEUF_MODE
        ) as datas:
            infos = datas.mydict("std nosep nonb")

        if GENE_TAG in infos:
            infos = infos[GENE_TAG]

            return infos.get(GENE_TNSLATEX_TAG, None) == YES_TAG

        return False









###
# prototype::
#     see = problems.Problems.new_error
# 
# This method is just an easy-to-use wrapper.
###
    def new_error(self, *args, **kwargs):
        self.success = False
        self.problems.new_error(*args, **kwargs)

###
# prototype::
#     see = problems.Problems.new_warning
# 
# This method is just an easy-to-use wrapper.
###
    def new_warning(self, *args, **kwargs):
        self.problems.new_warning(*args, **kwargs)

###
# prototype::
#     see = problems.Problems.resume
# 
# This method is just an easy-to-use wrapper.
###
    def resume(self, *args, **kwargs):
        self.problems.resume(*args, **kwargs)
