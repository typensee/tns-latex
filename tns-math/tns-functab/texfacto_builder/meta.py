from pathlib import Path
from yaml   import safe_load

from semver.version import Version

from .constants import *


# --------------------- #
# -- BUILD METADATAS -- #
# --------------------- #

def build_metadata(project_dir):
    metadata = {}

    proj_about = project_dir / "about.yaml"

    if not proj_about.is_file():
        raise IOError("missing an ''about.yaml'' for the project")


    with proj_about.open(
        encoding = 'utf8',
        mode     = 'r',
    ) as f:
        about_cfg = safe_load(f)

    gene_cfg = about_cfg["general"]

    metadata = {
        TAG_AUTHOR  : gene_cfg["author"],
        TAG_DESC    : gene_cfg["desc"],
        TAG_MANUAL_DEV_LANG: gene_cfg["lang"]["doc"],
    }

    metadata[TAG_MANUAL_OTHER_LANG] = manual_other_lang(
        project_dir = project_dir,
        dev_lang    = metadata[TAG_MANUAL_DEV_LANG]
    )

    metadata[TAG_PROJ_DIR]  = project_dir
    metadata[TAG_MANUAL]    = project_dir / "contrib" / "doc" / "manual"
    metadata[TAG_PROJ_NAME] = project_dir.name
    metadata[TAG_ROLLOUT]   = project_dir / "rollout"
    metadata[TAG_SRC]       = project_dir / "src"
    metadata[TAG_TEMP]      = project_dir / f".{metadata[TAG_PROJ_NAME]}"

    metadata[TAG_VERSIONS] = {
        TAG_ALL: about_stable_version(project_dir)
    }
    metadata[TAG_VERSIONS][TAG_LAST] = last_version(metadata[TAG_VERSIONS][TAG_ALL])

    metadata[TAG_CREATION] = creation(metadata[TAG_VERSIONS][TAG_ALL])

    return metadata


# -------------- #
# -- VERSIONS -- #
# -------------- #

def about_stable_version(project_dir):
    stable_chges_dir = project_dir / 'changes' / 'stable'

    stable_versions = {}

    for month_file in stable_chges_dir.glob("*/*.txt"):
        year  = month_file.parent.name
        month = month_file.stem

        content = month_file.read_text()

        match = re.search(DATE_PATTERN, content)

        if match:
            day     = match.group(1)
            version = match.group(2)

            stable_versions[version] = {
                TAG_DAY  : day,
                TAG_MONTH: month,
                TAG_YEAR : year,
            }

    stable_versions_revsorted = []

    all_nb_versions = [
        Version.parse(v)
        for v in stable_versions
    ]

    all_nb_versions.sort(reverse = True)

    for v in all_nb_versions:
        v = str(v)

        stable_versions_revsorted.append(
            stable_versions[v] | {TAG_NB: v}
        )

    return stable_versions_revsorted


def last_version(stable_versions):
    for v in stable_versions:
        break

    return v

def creation(stable_versions):
    for v in stable_versions:
        ...

    return v



# ----------------- #
# -- DOC. TRANS. -- #
# ----------------- #

def manual_other_lang(
    project_dir,
    dev_lang
):
    other_lang = []

    contrib_dir = project_dir / TAG_CONTRIB / TAG_DOC / TAG_MANUAL

    if not contrib_dir.is_dir():
        return other_lang

    status_dir = contrib_dir / TAG_STATUS

    if not status_dir.is_dir():
        raise IOError(
            f"missing ''{TAG_STATUS}'' folder. See the following dir.\n"
            f"{contrib_dir}")

    for yaml_file in status_dir.glob("*.yaml"):
        lang = yaml_file.stem

        if lang == dev_lang:
            continue

# Is the translation accpeted?
        with yaml_file.open(
            encoding = 'utf8',
            mode     = 'r',
        ) as f:
            lang_status = safe_load(f)

        if lang_status[TAG_STATUS] == TAG_STATUS_OK:
            other_lang.append(lang)

    return other_lang
