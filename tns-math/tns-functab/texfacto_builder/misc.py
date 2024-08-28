from datetime    import date
from babel.dates import format_date

from shutil   import rmtree

from .constants import *


# ----------------- #
# -- ASCII FRAME -- #
# ----------------- #

def frame(
    projname,
    title,
    extra = ""
):
    deco = '-'*(len(projname) + len(title) + 4)

    if extra:
        extra = " "*2 + extra

    return f"""
{deco}
"{projname}": {title}{extra}
{deco}
    """.strip()


def print_frame(
    projname,
    title,
    extra = ""
):
    print()
    print(frame(projname, title, extra))
    print()


# -------------------- #
# -- DATE / VERSION -- #
# -------------------- #

def nb_date_EN(dict_date):
    return (
        f"{dict_date[TAG_YEAR]}-"
        f"{dict_date[TAG_MONTH]}-"
        f"{dict_date[TAG_DAY]}"
    )


def short_name_date(
    dict_date,
    lang
):
    d = date(
        int(dict_date[TAG_YEAR]),
        int(dict_date[TAG_MONTH]),
        int(dict_date[TAG_DAY])
    )

    return format_date(d, locale = lang)


def date_n_version(
    dict_version,
    lang
):
    d = short_name_date(dict_version, lang)
    v = f"Version {dict_version[TAG_NB]}"

    dv = f"{d} - {v}"

    return dv


# ------------------- #
# -- OS OPERATIONS -- #
# ------------------- #

def emptydir(
    folder,
    rel_dir
):
    what = f"''{folder.relative_to(rel_dir)}'' folder."

    if folder.is_dir():
        print(f"+ Cleaning {what}")

        rmtree(folder)

    else:
        print(f"+ Creation of {what}")

    folder.mkdir(parents = True)


def createfile(file):
    file.parent.mkdir(
        parents  = True,
        exist_ok = True
    )

    file.touch()


def copyfromto(
    srcfile,
    destfile,
    mode = "w"
):
    with srcfile.open(
        encoding = "utf-8",
        mode = "r"
    ) as f:
        content = f.read()

    createfile(destfile)

    with destfile.open(
        encoding = "utf-8",
        mode     = mode
    ) as f:
        f.write(content)


def addcontentto(
    content,
    destfile
):
    with destfile.open(
        encoding = "utf-8",
        mode     = "a"
    ) as f:
        f.write(content)


def adddocsubdir(
    source,
    tmpdir,
    dirview,
    firstcall = True
):
    for onedir, dircontent in dirview.items():
        if firstcall and onedir.name == "locale":
            continue

        relpath = onedir.relative_to(source)

        if firstcall:
            print(f'   * [RES-DOC] Copying {relpath}/')

        destdir = tmpdir / relpath

        if not destdir.is_dir():
            destdir.mkdir(parents = True)

        for srcfile in dircontent[TAG_FILE]:
            copyfromto(srcfile, destdir / srcfile.name)

            TOC_DOC_RESRCES.append(srcfile)

        adddocsubdir(source, tmpdir, dircontent[TAG_DIR], firstcall=False)


# ----------------------- #
# -- SPECIFIC ITERATOR -- #
# ----------------------- #

def iter_sorted_useful_files(
    source,
    sorted_useful_files,
    ext_wanted,
    fake_src_name = ""
):
    if not fake_src_name:
        fake_src_name = source.name

    not_first_dir = False

    for onedir, files_n_resrc in sorted_useful_files.items():
        if not_first_dir:
            print()

        else:
            not_first_dir = True

        print(f'+ Working in {fake_src_name}/{onedir.relative_to(source)}/')

        for kind in [
            TAG_FILE,
            f"{ext_wanted}-{TAG_RESRC}"
        ]:
            for srcfile in files_n_resrc[kind]:
                ext = srcfile.suffix[1:]

                if ext != ext_wanted:
                    continue

                yield onedir, srcfile, kind
