from collections import defaultdict

from src2prod import *


TAG_FILE = "file"
TAG_DIR  = "dir"


def buildlof(
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
    lof = buildlof(
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
