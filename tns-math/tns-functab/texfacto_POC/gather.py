from collections import defaultdict
from shutil      import rmtree
from yaml        import safe_load

from natsort import natsorted


TAG_FILE = "file"
TAG_DIR  = "dir"

TAG_TOC  = "toc"

TAG_ABOUT_FILE = "about.yaml"

TAG_STY = "sty"
TAG_TEX = "tex"

TAG_CFG_STY = "cfg.sty"
TAG_CFG_TEX = "cfg.tex"


def dirs2analyze(
    source,
    alldirs
):
    src_about = source / "about.yaml"

    if not src_about.is_file():
        sorteddirs = None

    else:
        with src_about.open(
            encoding='utf8',
            mode='r',
        ) as f:
            about_cfg = safe_load(f)

        sorteddirs = about_cfg.get(TAG_TOC, None)

    if sorteddirs is None:
        sorteddirs = natsorted(alldirs)

    else:
        for i, p in enumerate(sorteddirs):
            if p[-1] != '/':
                TODO_PB

            p  = p[:-1]
            fp = source / p

            if not fp.is_dir():
                TODO_PB

            sorteddirs[i] = fp

    # print([p.name for p in sorting])

    return sorteddirs


def files2analyze(
    onedir,
    allfiles
):
    files_about = onedir / "about.yaml"

    if not files_about.is_file():
        sorted2analyze = None

    else:
        with files_about.open(
            encoding='utf8',
            mode='r',
        ) as f:
            about_cfg = safe_load(f)

        sorted2analyze = about_cfg.get(TAG_TOC, None)

    if sorted2analyze is None:
        sorted2analyze = natsorted(
            p
            for p in allfiles
            if p.suffix[1:] in [TAG_STY,TAG_TEX]
            and not p.suffix[1:] in [TAG_CFG_STY,TAG_CFG_TEX]
        )

    else:
        for i, p in enumerate(sorted2analyze):
            fp = onedir / p

            if not fp.is_file():
                TODO_PB

            sorted2analyze[i] = fp

    resources = [
        p
        for p in allfiles
        if not p in sorted2analyze
           and p.name != TAG_ABOUT_FILE
    ]

    # print([p.name for p in sorting])

    return sorted2analyze, resources


def emptydir(folder):
    if folder.is_dir():
        print(f'+ Cleaning {folder.parent.name}/{folder.name}')

        rmtree(folder)

    else:
        print(f'+ Creation of {folder.name}')

    folder.mkdir(parents = True)


def copyfromto(srcfile, destfile, mode="w"):
    with srcfile.open(
        encoding = "utf-8",
        mode = "r"
    ) as f:
        content = f.read()

    destfile.parent.mkdir(parents=True, exist_ok=True)
    destfile.touch()

    with destfile.open(
        encoding = "utf-8",
        mode = mode
    ) as f:
        f.write(content)


def addcontentto(content, destfile):
    with destfile.open(
        encoding = "utf-8",
        mode = "a"
    ) as f:
        f.write(content)


def extractfrom_STY(srcfile):
    with srcfile.open(
        encoding = "utf-8",
        mode = "r"
    ) as f:
        content = f.read()

    pack_import  = []
    pack_options = []
    pack_src     = []

    store_import  = "import"
    store_options = "options"
    store_src     = "src"
    store_ignore  = "ignore"
    store_in      = store_ignore

    for oneline in content.split('\n'):
        shortline = oneline.strip()

        if shortline == '% == PACKAGES == %':
            store_in = store_import
            continue

        if shortline == '% == OPTIONS == %':
            store_in = store_options
            continue

        if shortline == '% == TOOLS == %':
            store_in = store_src
            continue

        if store_in == store_import:
            pack_import.append(oneline)

        elif store_in == store_options:
            pack_options.append(oneline)

        elif store_in == store_src:
            pack_src.append(oneline)

    pack_import = '\n'.join(pack_import)
    pack_import = pack_import.strip()

    pack_options = '\n'.join(pack_options)
    pack_options = pack_options.strip()

    pack_src = '\n'.join(pack_src)
    pack_src = pack_src.strip()

    return pack_import, pack_options, pack_src


def prepare_STY(curdir, tmpdir, pack_import, pack_options, pack_src):
    if pack_import:
        pack_import += '\n'*3

        addcontentto(
            content  = pack_import,
            destfile = tmpdir / '.tmp_pack_import.sty'
        )

    if pack_options:
        pack_options += '\n'*3

        addcontentto(
            content  = pack_options,
            destfile = tmpdir / '.tmp_pack_options.sty'
        )

    if pack_src:
        pack_src = pack_src.replace(
            f"\\input{{../{curdir.name}/",
             "\\input{"
        )

        pack_src += '\n'*3

        addcontentto(
            content  = pack_src,
            destfile = tmpdir / '.tmp_pack_src.sty'
        )


def extractfrom_TEX(srcfile):
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

        if shortline == '% == FORDOC == %':
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


def prepare_TEX(_, tmpdir, fordoc, thedoc):
    if fordoc:
        fordoc += '\n'*3

        addcontentto(
            content  = fordoc,
            destfile = tmpdir / '.tmp_fordoc.tex'
        )

    if thedoc:
        thedoc += '\n'*3

        addcontentto(
            content  = thedoc,
            destfile = tmpdir / '.tmp_thedoc.tex'
        )


def adddocsubdir(source, tmpdir, dirview, firstcall=True):
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


EXTRACT_FROM = {
    TAG_STY: extractfrom_STY,
    TAG_TEX: extractfrom_TEX
}

PREPARE = {
    TAG_STY: prepare_STY,
    TAG_TEX: prepare_TEX
}

TOC_DOC         = []
TOC_DOC_RESRCES = []


def build_tmp_proj(
    source  ,
    treeview
):
    projectname = source.parent.name

    projectfolder_SRC  = source.parent / "src"
    projectfolder_TEMP = source.parent / f".{projectname}"

    sorteddirs = dirs2analyze(
        source  = source,
        alldirs = list(treeview[TAG_DIR].keys())
    )

    extradeco = "-"*(2 + len(projectname))

    print(f"""
---------------{extradeco}
"{projectname}": FINAL PRODUCT
---------------{extradeco}
    """)

    emptydir(projectfolder_TEMP)

    for onedir in sorteddirs:
        print(f'+ Working in src/{onedir.relative_to(source)}/')

        contentdir = treeview[TAG_DIR][onedir]

        sorted2analyze, resources = files2analyze(
            onedir   = onedir,
            allfiles = list(contentdir[TAG_FILE])
        )


        for srcfile in sorted2analyze:
            ext = srcfile.suffix[1:]

            print(
                f'   * [{ext.upper()}] Analyzing {srcfile.name}'
            )

            pieces = EXTRACT_FROM[ext](srcfile)
            PREPARE[ext](onedir, projectfolder_TEMP, *pieces)

            if ext == TAG_TEX:
                TOC_DOC.append(srcfile.relative_to(projectfolder_SRC))


        for srcfile in resources:
            print(
                f'   * [RES-SRC] Copying {srcfile.name}'
            )

            copyfromto(
                srcfile  = srcfile,
                destfile = projectfolder_TEMP / srcfile.name
            )


        adddocsubdir(onedir, projectfolder_TEMP, contentdir[TAG_DIR])


    codefile = projectfolder_TEMP / f"{projectname}.sty"
    code     = ''

    for tmpfile in [
        ".tmp_pack_import.sty",
        ".tmp_pack_options.sty",
        ".tmp_pack_src.sty",
    ]:
        with (projectfolder_TEMP / tmpfile).open(
            encoding = "utf-8",
            mode = "r"
        ) as f:
            code += f.read()

    code = code.strip()

    code = f"""
% ------------------------------------------------------- %
% - This is file `{projectname}.sty' generated automatically. - %
% -                                                     - %
% - Copyright (C) 2023-2024 by Christophe BAL           - %
% -                                                     - %
% - This file may be distributed and/or modified under  - %
% - the conditions of the GNU 3 License.                - %
% ------------------------------------------------------- %

\\ProvidesExplPackage
    {{{projectname}}}
    {{2024-01-06}} % Creation: 2023-11-29
    {{1.1.0}}
    {{This package proposes tools for writing "human friendly" documentations of LaTeX packages.}}

{code}
""".lstrip()

    with codefile.open(
        encoding = "utf-8",
        mode = "a"
    ) as f:
        f.write(code)


    codefile = projectfolder_TEMP / f"{projectname}-fr.tex"
    code     = r"""
\documentclass[10pt, a4paper]{article}

\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}

\usepackage[french]{babel, varioref}

\usepackage{enumitem}
\frenchsetup{StandardItemLabels=true}
    """.strip() + f"""

% Package documented.
\\usepackage[lang = french]{{{projectname}}}
    """.rstrip() + '\n'*3

    for tmpfile in [
        ".tmp_fordoc.tex",
        ".tmp_thedoc.tex",
    ]:
        if tmpfile == ".tmp_thedoc.tex":
            code += r"""
\begin{document}

\title{Le package \texttt{tutodoc} - Documentation de type tutoriel}
\author{Christophe BAL}
\date{1\ier{} Janv. 2024 - Version 1.1.0}

\maketitle

\begin{abstract}
Le package \tdocpack{tutodoc}
\footnote{
    Le nom vient de \tdocquote{\tdocprewhy{tuto.rial-type} \tdocprewhy{doc.umentation}} se traduit en \tdocquote{documentation de type tutoriel}.
}
est utilisé par son auteur pour produire de façon sémantique des documentations de packages et de classes \LaTeX\ dans un style de type tutoriel
\footnote{
    L'idée est de produire un fichier \texttt{PDF} efficace à parcourir pour des besoins ponctuels. C'est généralement ce que l'on attend d'une documentation liée au codage.
},
et avec un rendu sobre pour une lecture sur écran.


\begin{tdocnote}
     Ce package impose un style de mise en forme.
    Dans un avenir plus ou moins proche, \tdocpack{tutodoc} sera sûrement éclaté en une classe et un package.
\end{tdocnote}

\tdocsep

{\small\itshape
\textbf{Abstract.}
The \tdocpack{tutodoc} package
\footnote{
    The name comes from \tdocquote{\tdocprewhy{tuto.rial-type} \tdocprewhy{doc.umentation}}.
}
is used by its author to semantically produce documentation of \LaTeX\ packages and classes in a tutorial style
\footnote{
    The idea is to produce an efficient \texttt{PDF} file that can be browsed for one-off needs. This is generally what is expected of coding documentation.
},
and with a sober rendering for reading on screen.


\begin{tdocnote}
     This package imposes a formatting style. In the not-too-distant future, \tdocpack{tutodoc} will probably be split into a class and a package.
\end{tdocnote}
}
\end{abstract}


\newpage
\tableofcontents
\newpage
"""

        with (projectfolder_TEMP / tmpfile).open(
            encoding = "utf-8",
            mode = "r"
        ) as f:
            code += f.read()


    code = code.strip()
    code += r"""
\section{Historique}

\tdocversion{1.1.0}[2024-01-06]

\begin{tdocnew}
	\item Journal des changements : deux nouveaux environnements.
    \begin{enumerate}
        \item \tdocenv{tdocbreak} pour les \tdocquote{bifurcations}\,, soit les modifications non rétrocompatibles.

        \item \tdocenv{tdocprob} pour les problèmes repérés.
    \end{enumerate}

	\item \tdocmacro{tdocinlatex}: un jaune léger est utilisé comme couleur de fond.
\end{tdocnew}

\tdocsep

\tdocversion{1.0.1}[2023-12-08]

\begin{tdocfix}
	\item \tdocmacro{tdocenv}: l'espacement est maintenant correct, même si le paquet \tdocpack{babel} n'est pas chargé avec la langue française.

	\item \tdocenv[{[nostripe]}]{tdocshowcase}: les sauts de page autour des lignes \tdocquote{cadrantes} devraient être rares dorénavant.
\end{tdocfix}

\tdocsep

\tdocversion{1.0.0}[2023-11-29]

Première version publique du projet.

\end{document}
"""

    with codefile.open(
        encoding = "utf-8",
        mode = "a"
    ) as f:
        f.write(code)


    return projectfolder_TEMP
