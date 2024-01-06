import re

from pathlib import Path
from yaml import safe_load

from texfacto_POC import *


PROJECT_DIR    = Path(__file__).parent
PROJECT_NAME   = PROJECT_DIR.name
SOURCE_DIR     = PROJECT_DIR / 'src'
CONTRIB_DIR    = PROJECT_DIR / 'contrib' / 'api' / 'locale'
CONTRIB_STATUS = CONTRIB_DIR / 'status'


# --------------------- #
# -- CONTRIB. UPDATE -- #
# --------------------- #

for locdir in SOURCE_DIR.glob("*/locale/*"):
    lang = locdir.name
    ctxt = list(locdir.relative_to(SOURCE_DIR).parents)[1]

    print(f"+ Working in src/{locdir.relative_to(SOURCE_DIR)}")

    contribfolder = CONTRIB_DIR / lang / ctxt

    emptydir(contribfolder)

    for locfile in locdir.glob("*"):
        if not locfile.is_file():
            continue

        copyfromto(locfile, contribfolder / locfile.name)

# ---------------- #
# -- SRC UPDATE -- #
# ---------------- #

PATTERN_TEX_ARG = re.compile('#(\d+)')

def iter_texspec_from_esv(file):
    for oneline in file.read_text().split('\n'):
        oneline = oneline.strip()

        if not oneline or oneline[:2] == '//':
            continue

        macroname, _, texcode = oneline.partition('=')

        macroname = macroname.strip()
        texcode   = texcode.strip()

        nbparams = 0

        for m in PATTERN_TEX_ARG.finditer(texcode):
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

all_status = {}

for langfile in CONTRIB_STATUS.glob("*"):
    if not langfile.is_file() or langfile.name[0] == "." or langfile.suffix != ".yaml":
        continue

    with open(langfile,'r') as f:
        all_status[langfile.stem] = safe_load(f)


for langdir in CONTRIB_DIR.glob("*"):
    if (
        not langdir.is_dir()
        or
        not langdir.stem in all_status
        or
        all_status[langdir.stem]['status'] != "ok"
    ):
        continue


    print(f'+ Updating from "{langdir.relative_to(CONTRIB_DIR)}" contrib.')

    for ctxt in langdir.glob("*"):
        if not ctxt.is_dir() or ctxt.name[0] == ".":
            continue

        print(f'    * Updating "{PROJECT_NAME}/src/{ctxt.name}".')

        langname = all_status[langdir.stem].get("lang-api", langdir.stem)

        stycfgfile = SOURCE_DIR / ctxt.name
        stycfgfile /= f"{PROJECT_NAME}-locale-{ctxt.stem}-{langname}.cfg.sty"

        texmacros = []

        for esvfile in ctxt.glob("*.txt"):
            texmacros += extractesv(PROJECT_NAME, esvfile)

        texmacros = "\n".join(texmacros)

        stycfgfile.touch()
        stycfgfile.write_text(data = texmacros)
