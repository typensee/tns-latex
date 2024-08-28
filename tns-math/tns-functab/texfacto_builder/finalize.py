from .constants import *
from .misc      import *


# --------------------------- #
# -- END IS COMING SOON... -- #
# --------------------------- #

def finalize(
    metadata,
    ugly_hack = lambda x:x
):
    final_sty(metadata)

    print()

    final_tex(metadata, ugly_hack)


def final_tex(metadata, ugly_hack):
    doc_dir  = metadata[TAG_ROLLOUT] / "doc"

    emptydir(
        folder  = doc_dir,
        rel_dir = metadata[TAG_PROJ_DIR]
    )

    for lang in metadata[TAG_TEMP].glob("*"):
        if not lang.is_dir():
            continue

        lang = lang.name

        print(f"+ Building ''{lang}'' TEX file.")

        code_file = doc_dir / f"{metadata[TAG_PROJ_NAME]}-{lang}.tex"

        old_2_new_path, resrc = tex_resrc(
            lang,
            metadata
        )

        header = tex_header(
            lang,
            metadata
        )

        main = tex_main(
            lang,
            metadata
        )

        old_main = main.split('\n')
        main     = []

        for line in old_main:
            newline = line

            for pattern in CMDS_FOR_FILE_PATTERNS:
                match = pattern.findall(line)

                if not match:
                    continue

                start, comment, macroname, options, input_file, end = match[0]

                if input_file == '#1':
                    continue

                if comment:
                    continue

                for old in "./":
                    input_file_cleaned = input_file.replace(old, '-')

                newline = f"{start}{macroname}{options}{{{input_file_cleaned}}}{end}\n"

                break

                f_out.write(newline)

            main.append(newline)

        main = '\n'.join(main)
        main = ugly_hack(main)

        resrc = ugly_hack(resrc)

        code = f"""
{resrc}


{header}


{main}
        """.strip() + '\n'

        code_file.write_text(code)


def tex_header(
    lang,
    metadata
):
    lang_dir = metadata[TAG_TEMP] / lang

    preamble = (lang_dir / TAG_TMP_PREAMBLE).read_text()
    preamble = preamble.strip()

    fordoc = (lang_dir / TAG_TMP_TEX_FOR_DOC).read_text()
    fordoc = fordoc.strip()

    title = pretty_title(
        deco  = "=",
        title = "SOURCE FOR THE DOC"
    )

    header = f"""{title}

\\documentclass[10pt, a4paper]{{article}}

{preamble}


{fordoc}


\\begin{{document}}
    """.strip()

    return header


def tex_main(
    lang,
    metadata
):
    lang_dir = metadata[TAG_TEMP] / lang

    manual = (lang_dir / TAG_TMP_TEX_THE_DOC).read_text()
    manual = manual.strip()

    abstract = (lang_dir / f"{TAG_ABSTRACT}.tex").read_text()
    abstract = abstract.strip()

    for old, new in {
        'AUTHOR'        : metadata[TAG_AUTHOR],
        'DATE-N-VERSION': date_n_version(
            metadata[TAG_VERSIONS][TAG_LAST],
            lang
        ),
    }.items():
        abstract = abstract.replace(f"<<{old}>>", new)


    chgelog = (lang_dir / f"{TAG_CHGE_LOG}.tex").read_text()
    chgelog = chgelog.strip()

    main = f"""
{abstract}


\\newpage
\\tableofcontents
\\newpage


{manual}


\\section{{{HISTORY_TRANS[lang]}}}

{chgelog}

\\end{{document}}
    """.strip() + '\n'

    return main



def tex_resrc(
    lang,
    metadata
):
    lang_dir = metadata[TAG_TEMP] / lang

    resrc        = []
    old_2_new_path = {}

    for resrc_dir in lang_dir.glob("*"):
        if (
            not resrc_dir.is_dir()
            or
            resrc_dir.name[0] == "."
        ):
            continue

        for resrc_file in resrc_dir.rglob("*"):
            if (
                not resrc_file.is_file()
                or
                resrc_file.name[0] == "."
            ):
                continue

            old_path = str(resrc_file.relative_to(lang_dir))
            new_path = old_path.replace("/", "-")

            old_2_new_path[old_path] = new_path

            resrc.append(
                f"""
\\begin{{filecontents*}}[overwrite]{{{new_path}}}
{resrc_file.read_text().strip()}
\\end{{filecontents*}}
                """.strip()
            )

    resrc = [
        pretty_title(
            deco  = "=",
            title = "RESOURCES USED"
        )
    ] + resrc

    resrc = '\n\n\n'.join(resrc)


    return old_2_new_path, resrc


def final_sty(metadata):
    code_dir  = metadata[TAG_ROLLOUT] / "code"

    emptydir(
        folder  = code_dir,
        rel_dir = metadata[TAG_PROJ_DIR]
    )

    print("+ Building STY file.")

    code_file = code_dir / f"{metadata[TAG_PROJ_NAME]}.sty"

    code = [sty_header(metadata)]

    for kind, temp_file in [
        ("PACKAGES USED"    , TAG_TMP_STY_IMPORT),
        ("AVAILABLE OPTIONS", TAG_TMP_STY_OPTIONS),
        ("MAIN CODE"        , TAG_TMP_STY_SRC),
    ]:
        code.append(
            f"""
% == {kind} == %

{(metadata[TAG_TEMP] / temp_file).read_text()}
            """.rstrip()
        )

    code = '\n\n'.join(code)
    code = code.strip() + '\n'

    code = prettify_all_titles(code)

    code_file.write_text(code)

    print("+ Copying STY resources.")

    for resrc in metadata[TAG_TEMP].glob("*.sty"):
        if resrc.name[0] == '.':
            continue

        copyfromto(
            srcfile  = resrc,
            destfile = code_dir / resrc.name
        )


def sty_header(metadata):
# About
    about = SRC_CODE_HEADER

    for old, new in {
        'PROJ_NAME'    : metadata[TAG_PROJ_NAME],
        'CREATION_YEAR': metadata[TAG_CREATION][TAG_YEAR],
        'LAST_YEAR'    : metadata[TAG_VERSIONS][TAG_LAST][TAG_YEAR],
        'AUTHOR'       : metadata[TAG_AUTHOR],
    }.items():
        about = about.replace(f"<<{old}>>", new)

    about = about.split('\n')

    max_len = max(len(l) for l in about)

    for i, line in enumerate(about):
        line += ' ' * (max_len - len(line))
        line  = f"% ** {line} ** %"

        about[i] = line

    about = '\n'.join(about)

    deco =  '*' * (max_len + 6)
    deco  = f"% {deco} %"

    about = f"""
{deco}
{about}
{deco}
    """.strip()

# Provide package
    provide = SRC_CODE_PROVIDE_PACK

    for old, new in {
        'PROJ_NAME'    : metadata[TAG_PROJ_NAME],
        'CREATION_DATE': nb_date_EN(metadata[TAG_CREATION]),
        'LAST_DATE'    : nb_date_EN(metadata[TAG_VERSIONS][TAG_LAST]),
        'LAST_NB_VER'  : metadata[TAG_VERSIONS][TAG_LAST][TAG_NB],
        'SHORT_DESC'   : metadata[TAG_DESC],
    }.items():
        provide = provide.replace(f"<<{old}>>", new)

    return f"""
{about}

{provide}
    """.strip()


def prettify_all_titles(code):
    new_code   = []
    not_ignore = False

    for line in code.split('\n'):
        if line == r"\ProvidesExplPackage":
            not_ignore = True

        if not_ignore:
            for pattern in TITLE_PATTERNS:
                match = re.search(pattern, line)

                if match:
                    title     = match.group(2)
                    pre_deco  = match.group(1)
                    # post_deco = match.group(3)

                    line = pretty_title(
                        pre_deco[0],
                        title
                    )

                    break

        new_code.append(line)

    new_code = '\n'.join(new_code)

    return new_code


def pretty_title(
    deco,
    title
):
    rule = deco * (len(title) + 6)
    rule = f"% {rule} %"

    title = f"""
{rule}
% {deco*2} {title} {deco*2} %
{rule}
    """.strip()

    return title
