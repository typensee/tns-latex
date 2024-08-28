DEBUG = False
# DEBUG = True


# ------------------- #
# -- PACKAGES USED -- #
# ------------------- #

from src2prod import *

from texfacto_builder import *

if DEBUG:
    from pprint import pprint


# --------------- #
# -- CONSTANTS -- #
# --------------- #

THIS_DIR = Path(__file__).parent

WHAT = "[CONTRIB. to MAIN]"


# ---------------------- #
# -- METADATA PROJECT -- #
# ---------------------- #

print_frame(
    THIS_DIR.name,
    "METADATA"
)

metadata = build_metadata(project_dir = THIS_DIR)

if DEBUG:
    print("# -- METADATA -- #")

    pprint(metadata)
    # exit()

print(f"Dev lang : {metadata[TAG_MANUAL_DEV_LANG]}")
print()

# exit()


# ----------------------- #
# -- ALL USEFULL FILES -- #
# ----------------------- #

treeview = build_tree(
    project = metadata[TAG_PROJ_DIR],
    source  = metadata[TAG_SRC],
    target  = metadata[TAG_ROLLOUT],
    readme  = Path('README.md'),
    ignore = """
test_*/
tests_*/
test_*.*
tests_*.*

tool_*/
tools_*/
tool_*.*
tools_*.*
"""
)

for directdir, content in treeview[TAG_DIR].items():
    subfiles = content[TAG_FILE]

# We need to work on a copy of ''subfiles''.
    for directsubfile in subfiles[:]:
        if directsubfile.suffix == '.tex':
            pdf_unused = directsubfile.parent / f"{directsubfile.stem}.pdf"

            if pdf_unused in subfiles:
                subfiles.remove(pdf_unused)


# ---------------------- #
# -- USEFUL CONSTANTS -- #
# ---------------------- #

SRC_DIR = metadata[TAG_SRC]

CONTRIB_DIR        = metadata[TAG_PROJ_DIR] / TAG_CONTRIB
CONTRIB_API_DIR    = CONTRIB_DIR / TAG_API / TAG_LOCALE
CONTRIB_STATUS_DIR = CONTRIB_API_DIR / 'status'

PROJECT_NAME = metadata[TAG_PROJ_NAME]


# ----------- #
# -- TOOLS -- #
# ----------- #

def iter_texspec_from_esv(file):
    for oneline in file.read_text().split('\n'):
        oneline = oneline.strip()

        if not oneline or oneline[:2] == '//':
            continue

        macroname, _, texcode = oneline.partition('=')

        macroname = macroname.strip()
        texcode   = texcode.strip()

        nbparams = 0

        for m in CMD_ARG_PATTERN.finditer(texcode):
            nbparams = max(nbparams, int(m.group(1)))

        yield nbparams, macroname, texcode


def extractesv(projname, file):
    if not file.stem in ["macros", "sentences"]:
        return []

    macrodefs = []

    for nbparams, macroname, texcode in iter_texspec_from_esv(file):
        signature = "m"*nbparams
        macroname = macroname.replace('_', '@')
        texcode   = texcode.replace(' ', ' ~ ')

        macrodefs.append(
            f"\\NewDocumentCommand{{\\{projname}@trans@{macroname}}}"
            f"{{{signature}}}{{{texcode}}}"
        )

    return macrodefs


# ------------------ #
# -- API CONTRIB. -- #
# ------------------ #

print_frame(
    metadata[TAG_PROJ_NAME],
    "API",
    WHAT
)


all_status = {}

for lang_file in CONTRIB_STATUS_DIR.glob("*"):
    if (
        not lang_file.is_file()
        or
        lang_file.name[0] == "."
        or
        lang_file.suffix != ".yaml"
    ):
        continue

    with open(lang_file,'r') as f:
        all_status[lang_file.stem] = safe_load(f)


first_dir = True

for lang_dir in CONTRIB_API_DIR.glob("*"):
    lang = lang_dir.name

    if (
        lang == "status"
        or
        not lang in all_status
    ):
        continue

    if first_dir:
        first_dir = False
    else:
        print()

    lang_status = all_status[lang]

    if lang_status[TAG_STATUS] != TAG_STATUS_OK:
        print(f"+ Rejected translation : ''contrib/api/locale/{lang}''")

        continue

    print(f"+ Accepted translation : ''contrib/api/locale/{lang}''")


    for ctxt in lang_dir.glob("*"):
        if (
            not ctxt.is_dir()
            or
            ctxt.name[0] == "."
        ):
            continue

        print(f'    * Updating "/src/{ctxt.name}".')

        lang_full = LANG_NAMES[TAG_LANG_EN][lang].lower()

        sty_cfg  = SRC_DIR / ctxt.name
        sty_cfg /= f"{PROJECT_NAME}-locale-{ctxt.stem}-{lang_full}.cfg.sty"

        texmacros = []

        for esvfile in ctxt.glob("*.txt"):
            texmacros += extractesv(PROJECT_NAME, esvfile)

        texmacros = "\n".join(texmacros)

        createfile(sty_cfg)
        sty_cfg.write_text(texmacros)
