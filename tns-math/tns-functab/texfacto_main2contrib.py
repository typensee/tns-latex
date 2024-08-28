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

WHAT = "[MAIN to CONTRIB.]"


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


# ----------------------- #
# -- SORTED MAIN FILES -- #
# ----------------------- #

print_frame(
    metadata[TAG_PROJ_NAME],
    "SORTED MAIN FILES",
    "(no resources printed)"
)

sorted_useful_files = files_2_analyze(
    source   = metadata[TAG_SRC],
    treeview = treeview
)

if DEBUG:
    for onedir, sorted2analyze in sorted_useful_files.items():
        print()
        print()
        print(f"+ {onedir}")
        print()
        pprint(sorted2analyze)

    exit()

# -------------------- #
# -- USEFUL FOLDERS -- #
# -------------------- #

SRC_DIR = metadata[TAG_SRC]

CONTRIB_DIR        = metadata[TAG_PROJ_DIR] / TAG_CONTRIB
CONTRIB_API_DIR    = CONTRIB_DIR / TAG_API / TAG_LOCALE
CONTRIB_DEV_MANUAL_DIR = CONTRIB_DIR / TAG_DOC / TAG_MANUAL / metadata[TAG_MANUAL_DEV_LANG]


# ------------------ #
# -- API CONTRIB. -- #
# ------------------ #

print_frame(
    metadata[TAG_PROJ_NAME],
    "API",
    WHAT
)

glob_search = f"*/{TAG_LOCALE}/*"
first_dir   = True

for locale_dir in metadata[TAG_SRC].glob(glob_search):
    lang = locale_dir.name
    ctxt = list(
        locale_dir.relative_to(metadata[TAG_SRC]).parents
    )[1]

    if first_dir:
        first_dir = False
    else:
        print()

    print(f"+ Working in ''src/{locale_dir.relative_to(metadata[TAG_SRC])}''")

    this_contrib_dir = CONTRIB_API_DIR / lang / ctxt

    emptydir(
        folder  = this_contrib_dir,
        rel_dir = CONTRIB_DIR
    )

    for locale_file in locale_dir.glob("*"):
        if (
            not locale_file.is_file()
            or
            locale_file.name[0] == "."
        ):
            continue

        copyfromto(locale_file, this_contrib_dir / locale_file.name)

    print(f"+ Update done.")


# ------------------ #
# -- DOC CONTRIB. -- #
# ------------------ #

print_frame(
    metadata[TAG_PROJ_NAME],
    "DOC",
    WHAT
)


# Empty lang dir.
emptydir(
    folder  = CONTRIB_DEV_MANUAL_DIR,
    rel_dir = metadata[TAG_PROJ_DIR],
)

# Preamble file.
print(f"+ Building ''src/{TAG_TMP_PREAMBLE}''")

contrib_preamble = CONTRIB_DEV_MANUAL_DIR / TAG_TMP_PREAMBLE

copyfromto(
    srcfile  = SRC_DIR / TAG_TMP_PREAMBLE,
    destfile = contrib_preamble
)

content = contrib_preamble.read_text()

new_content    = []
contrib_import = False

for line in content.split('\n'):
    short_line = line.strip()

    if line == TAG_MC_CONTRIB_LOAD:
        contrib_import = True

        line = "% Package documented."

    elif contrib_import and short_line:
        line = line[2:]

    new_content.append(line)

new_content = '\n'.join(new_content)

contrib_preamble.write_text(new_content)

# Change log.
print(f"+ Building ''src/{TAG_CHGE_LOG}''")

for srcfile in (SRC_DIR / TAG_CHGE_LOG).glob("*/*/*.tex"):
    day   = srcfile.stem
    month = srcfile.parent.name
    year  = srcfile.parent.parent.name

    destfile = CONTRIB_DEV_MANUAL_DIR / TAG_CHGE_LOG / year / f"{month}-{day}.tex"

    content = srcfile.read_text().strip()
    content = f"""
\\documentclass[12pt, a4paper]{{article}}

\\input{{../../preamble.cfg.tex}}


\\begin{{document}}

{content}

\\end{{document}}
    """.strip() + "\n"

    createfile(destfile)
    destfile.write_text(content)

# Manual TEX files.
print("+ Copying manual TEX files...")

all_tex_files = [SRC_DIR / TAG_ABSTRACT / f"{TAG_ABSTRACT}.tex"]

for onedir, sorted2analyze in sorted_useful_files.items():
    for srcfile in sorted2analyze[TAG_FILE]:
        if srcfile.suffix[1:] != TAG_TEX:
            continue

        all_tex_files.append(srcfile)


for srcfile in all_tex_files:
    fordoc, thedoc = extract_from_TEX(srcfile)

    if fordoc:
        fordoc = f"\n{fordoc}\n"

    content = f"""
\\documentclass[12pt, a4paper]{{article}}

\\input{{../preamble.cfg.tex}}
{fordoc}

\\begin{{document}}

{thedoc}

\\end{{document}}
    """.strip() + "\n"

    destfile = CONTRIB_DEV_MANUAL_DIR / srcfile.relative_to(SRC_DIR)

    createfile(destfile)
    destfile.write_text(content)

# TEX resources.
print("+ Copying TEX resources...")

for onedir, sorted2analyze in sorted_useful_files.items():
    for srcfile in sorted2analyze[TAG_TEX_RESRC]:
        copyfromto(
            srcfile  = srcfile,
            destfile = CONTRIB_DEV_MANUAL_DIR / srcfile.relative_to(SRC_DIR)
        )
