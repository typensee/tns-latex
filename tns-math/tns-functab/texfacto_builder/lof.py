from collections import defaultdict
from yaml        import safe_load

from src2prod import *

from .constants import *


# ----------------- #
# -- "ALL" FILES -- #
# ----------------- #

def build_full_lof(
    project,
    source,
    target,
    readme,
    ignore = '',
):
    project = Project(
        project = project,
        source  = source,
        target  = target,
        usegit  = True,
        readme  = readme,
        ignore  = ignore,
    )

    project.build()

    return [f for f in project.lof]


def build_tree(
    project,
    source,
    target,
    readme,
    ignore = '',
):
    lof = build_full_lof(
        project = project,
        source  = source,
        target  = target,
        readme  = readme,
        ignore  = ignore,
    )

    return _recu_build_tree(
        current_dir = project / source,
        lof    = lof
    )

def _recu_build_tree(
    current_dir,
    lof,
):
    treeview        = defaultdict(list)
    pre_subtreeview = defaultdict(list)
    subtreeview     = {}

    for f in lof:
# Don't forget the use of PosixPath('.').
        parents = list(f.relative_to(current_dir).parents)[:-1]
        depth   = len(parents)

        if depth == 0:
            treeview[TAG_FILE].append(f)

        else:
            pre_subtreeview[parents[-1]].append(f)

    for subfolder, sublof in pre_subtreeview.items():
        subtreeview[current_dir / subfolder] = _recu_build_tree(
            current_dir = current_dir / subfolder,
            lof         = sublof,
        )

    treeview[TAG_DIR] = subtreeview

    return treeview


# -------------------- #
# -- "USEFUL" FILES -- #
# -------------------- #

def dirs_2_analyze(
    source,
    alldirs
):
    src_about = source / "about.yaml"

    if not src_about.is_file():
        sorteddirs = None

    else:
        with src_about.open(
            encoding = 'utf8',
            mode     = 'r',
        ) as f:
            about_cfg = safe_load(f)

        sorteddirs = about_cfg.get(TAG_TOC, None)

    if sorteddirs is None:
        sorteddirs = natsorted(alldirs)

    else:
        for i, p in enumerate(sorteddirs):
            if p[-1] != '/':
                raise ValueError(
                     "path for folders expected in the TOC of "
                    f"the following file.\n{src_about}"
                )

            p  = p[:-1]
            fp = source / p

            if not fp.is_dir():
                raise IOError(
                     "the following path does not point to a folder"
                    f"\n{fp}"
                )

            sorteddirs[i] = fp

    # print([p.name for p in sorting])

    return sorteddirs


def loc_files_2_analyze(
    onedir,
    allfiles
):
# 1st level files
    files_about = onedir / "about.yaml"

    if not files_about.is_file():
        sorted2analyze = None

    else:
        with files_about.open(
            encoding = 'utf8',
            mode     = 'r',
        ) as f:
            about_cfg = safe_load(f)

        sorted2analyze = about_cfg.get(TAG_TOC, None)

    if sorted2analyze is None:
        sorted2analyze = natsorted(
            p
            for p in allfiles
            if (
                p.suffix[1:] in [TAG_STY,TAG_TEX]
                and
                not p.suffix[1:] in [TAG_CFG_STY,TAG_CFG_TEX]
            )
        )

    else:
        for i, p in enumerate(sorted2analyze):
            fp = onedir / p

            if not fp.is_file():
                TODO_PB

            sorted2analyze[i] = fp

    resources = {
        TAG_STY: [
            p
            for p in allfiles
            if (
                not p in sorted2analyze
                and
                p.name != TAG_ABOUT_FILE
            )
        ],
# Searching for doc resources
        TAG_TEX: [
            p
            for p in onedir.rglob("*")
            if (
                p.is_file()
                and
                not ignore_this(onedir, p)
            )
        ]
    }

# Nothing left to do.
    return sorted2analyze, resources


def ignore_this(
    onedir,
    pfile
):
    if (
        pfile.parent == onedir
        or
        pfile.parent.name.startswith("_minted-")
        or
        pfile.parent.parent.name == "locale"
        or
        pfile.name == TAG_ABOUT_FILE
    ):
        return True

    return False


def files_2_analyze(
    source,
    treeview
):
    sorted_useful_files = {}

    not_first_dir = False

    for onedir in dirs_2_analyze(
        source  = source,
        alldirs = list(treeview[TAG_DIR].keys())
    ):
        if not_first_dir:
            print()

        else:
            not_first_dir = True

        print(f'+ src/{onedir.relative_to(source)}/')

        contentdir = treeview[TAG_DIR][onedir]

        sorted2analyze, resources = loc_files_2_analyze(
            onedir   = onedir,
            allfiles = list(contentdir[TAG_FILE])
        )

        for srcfile in sorted2analyze:
            print(f"  * {srcfile.name}")

        print(
               "  * RESOURCES: "
            + f"{TAG_STY.upper()} = {len(resources[TAG_STY])}"
            +  "\n" + " "*len("  * RESOURCES: ")
            + f"{TAG_TEX.upper()} = {len(resources[TAG_TEX])}"
        )

        sorted_useful_files[onedir] = {
            TAG_FILE     : sorted2analyze,
            TAG_STY_RESRC: resources[TAG_STY],
            TAG_TEX_RESRC: resources[TAG_TEX],
        }

    return sorted_useful_files
