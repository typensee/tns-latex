from .constants import *
from .misc      import *


# --------------------------- #
# -- BUILD SINGLE STY FILE -- #
# --------------------------- #

def prebuild_single_tex(
    source,
    temp_dir,
    sorted_useful_files,
    dev_lang,
    other_lang,
    versions
):
    all_langs   = [dev_lang] + other_lang
    contrib_dir = source.parent / TAG_CONTRIB / TAG_DOC / TAG_MANUAL

# English abstract.
    if not TAG_LANG_EN in all_langs:
        print(f"+ Abstract: no English!")

    else:
        print(f"+ Abstract: English version.")

        abstract_EN = abstract_of(
            lang        = TAG_LANG_EN,
            contrib_dir = contrib_dir
        )

        abstract_EN = "\n    ".join(
            abstract_EN.split("\n")
        )

        abstract_EN = other_langs(
            content   = abstract_EN,
            lang      = TAG_LANG_EN,
            all_langs = all_langs
        )

# Let's work lang by lang.
    for i, lang in enumerate(all_langs, 0):
        print()

        kind = "dev." if i == 0 else "contrib."

        print(f"## {kind.upper()} LANG ''{lang}'' ##")
        print()

        lang_dir      = contrib_dir / lang
        lang_temp_dir = temp_dir / lang

# Empty lang dir.
        emptydir(
            folder  = lang_temp_dir,
            rel_dir = source.parent
        )

# Preamble file.
        print()
        print(f"+ [RES-TEX] Copying ''{lang}/{TAG_TMP_PREAMBLE}''")

        copyfromto(
            srcfile  = lang_dir / TAG_TMP_PREAMBLE,
            destfile = lang_temp_dir / TAG_TMP_PREAMBLE
        )

# Change log.
        print()
        print(f"+ Change log")

        chge_dir = lang_dir / TAG_CHGE_LOG
        content  = []

        for vers in versions[TAG_ALL]:
            print(
                f"    * {vers[TAG_YEAR]}-{vers[TAG_MONTH]}-{vers[TAG_DAY]}  "
                f"[{vers[TAG_NB]}]"
            )

            chge_file = (
                chge_dir / vers[TAG_YEAR] / f"{vers[TAG_MONTH]}-{vers[TAG_DAY]}.tex"
            )

            if not chge_file.is_file():
                raise IOError(
                    f"missing file.\n{chge_file.relative_to(lang_dir)}"
                )

            about_this_change = content_from_TEX(chge_file)

            content.append(
                f"""
\\tdocversion{{{vers[TAG_NB]}}}[{nb_date_EN(vers)}]

{about_this_change}
                """.strip()
            )

        content = "\n\n\\tdocsep\n\n\n% ------------------ %\n\n\n".join(content)
        content = content.strip()

        chge_file = lang_temp_dir / f"{TAG_CHGE_LOG}.tex"
        chge_file.write_text(content)

# Abstract.
        abstract = content_from_TEX(
            srcfile = contrib_dir / lang / TAG_ABSTRACT / f"{TAG_ABSTRACT}.tex"
        )

        if lang != TAG_LANG_EN:
            abstract = abstract.replace(
                "\\end{abstract}",
                f"""
    \\tdocsep

    {{\\small\\itshape
        \\textbf{{Abstract.}}
        {abstract_EN}
    }}
\\end{{abstract}}
                """.rstrip()
            )

        abstract = other_langs(
            content   = abstract,
            lang      = lang,
            all_langs = all_langs
        )

        abstract_file = lang_temp_dir / f"{TAG_ABSTRACT}.tex"
        abstract_file.write_text(abstract)

# Manual.
        print()

        for onedir, srcfile, kind in iter_sorted_useful_files(
            source              = source,
            sorted_useful_files = sorted_useful_files,
            ext_wanted          = TAG_TEX,
            fake_src_name       = lang
        ):
            curdir  = lang_dir / onedir.name
            srcfile = curdir / srcfile.relative_to(onedir)

            if kind == TAG_FILE:
                print(f"   * Analyzing ''{srcfile.name}''")

# WARNING!
# No magic comment inside the manual of the dev contrib.
                thedoc = srcfile.read_text()

                _     , _, thedoc = thedoc.partition("\\input{../preamble.cfg.tex}")
                fordoc, _, thedoc = thedoc.partition("\\begin{document}")
                thedoc, _, _      = thedoc.partition("\\end{document}")

                fordoc = fordoc.strip()
                thedoc = thedoc.strip()

                pieces = extract_from_DEV_TEX(srcfile)
                prepare_TEX(onedir, lang_temp_dir, fordoc, thedoc)

            else:
                relpath = srcfile.relative_to(curdir)

                print(f"   * [RES-TEX] Copying ''{relpath}'")

                copyfromto(
                    srcfile  = srcfile,
                    destfile = lang_temp_dir / relpath
                )


def content_from_TEX(
    srcfile,
    start_block = "\\begin{document}",
    end_block   = "\\end{document}"
):
    content  = []
    store_in = False

    for oneline in srcfile.read_text().split('\n'):
        shortline = oneline.strip()

        if shortline == start_block:
            store_in = True
            continue

        if shortline == end_block:
            break

        if store_in:
            content.append(oneline)


    content = "\n".join(content)
    content = content.strip()

    return content


def extract_from_DEV_TEX(srcfile):
    with srcfile.open(
        encoding = "utf-8",
        mode = "r"
    ) as f:
        content = f.read()

    fordoc = []
    thedoc = []

    store_fordoc = "fordoc"
    store_thedoc = "thedoc"
    store_ignore = "ignore"
    store_in     = store_ignore

    for oneline in content.split('\n'):
        shortline = oneline.strip()

        if shortline == TAG_MC_FORDOC:
            store_in = store_fordoc
            continue

        if shortline == '\\begin{document}':
            store_in = store_thedoc
            continue

        if shortline == '\\end{document}':
            break

        if store_in == store_fordoc:
            fordoc.append(oneline)

        elif store_in == store_thedoc:
            thedoc.append(oneline)

    fordoc = '\n'.join(fordoc)
    fordoc = fordoc.strip()

    thedoc = '\n'.join(thedoc)
    thedoc = thedoc.strip()

    return fordoc, thedoc


def prepare_TEX(
    _     ,  # factorization needs ths unused argument...
    tmpdir,
    fordoc,
    thedoc
):
    fordoc_file = tmpdir / '.tmp_fordoc.tex'
    thedoc_file = tmpdir / '.tmp_thedoc.tex'

    createfile(fordoc_file)
    createfile(thedoc_file)

    if fordoc:
        fordoc += '\n'*3

        addcontentto(
            content  = fordoc,
            destfile = fordoc_file
        )

    if thedoc:
        thedoc += '\n'*3

        addcontentto(
            content  = thedoc,
            destfile = thedoc_file
        )



def other_langs(
    content,
    lang,
    all_langs,
):
    others = [
        LANG_NAMES[lang][l]
        for l in all_langs
        if l != lang
    ]

    content = content.replace(
        "<<OTHER-LANGS>>",
        ", ".join(others)
    )

    return content


def abstract_of(
    lang,
    contrib_dir
):
    abstract_file = contrib_dir / lang / TAG_ABSTRACT / f"{TAG_ABSTRACT}.tex"

    if not abstract_file.is_file():
        raise IOError("missing file.\n{abstract_file}")

    return content_from_TEX(
        srcfile     = abstract_file,
        start_block = f"\\begin{{{TAG_ABSTRACT}}}",
        end_block   = f"\\end{{{TAG_ABSTRACT}}}"
    )
