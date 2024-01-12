from collections import defaultdict
import                  re
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


STY_TITLES_PATTERNS = {
    deco: re.compile(
        f"% (?P<deco>{deco}){deco}[ \t]+(?P<title>.*)[ \t]+{deco*2} %"
    )
    for deco in "=-:"
}


def titlize(match_obj):
    if match_obj.group() is not None:
        founded = match_obj.group()
        rule    = match_obj.group('deco')*(
            2*3 + len(match_obj.group('title'))
        )

        return f"% {rule} %\n{founded}\n% {rule} %"


def prettySTY(code):
    for d, p in STY_TITLES_PATTERNS.items():
        code = re.sub(
            p,
            titlize,
            code
        )

    return code

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
                print(f"{sorteddirs = }")
                TODO_PB

            p  = p[:-1]
            fp = source / p

            if not fp.is_dir():
                print(f"{sorteddirs = }")
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
                print(f"{sorted2analyze = }")
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
            if srcfile.name.startswith("debug-"):
                continue

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
        tmpfile = projectfolder_TEMP / tmpfile

        if not tmpfile.is_file():
            continue

        with tmpfile.open(
            encoding = "utf-8",
            mode = "r"
        ) as f:
            code += f.read()

    code = code.strip()

    code = f"""
% ----------------------------------------------------------- %
% - This is file `{projectname}.sty' generated automatically. - %
% -                                                         - %
% - Copyright (C) 2024 by Christophe BAL                    - %
% -                                                         - %
% - This file may be distributed and/or modified under      - %
% - the conditions of the GNU 3 License.                    - %
% ----------------------------------------------------------- %

\\ProvidesExplPackage
    {{{projectname}}}
    {{2024-01-01}} % Creation: 2024-01-???
    {{1.0.0}}
    {{This package proposes ???.}}

{code}
""".lstrip()

    code = prettySTY(code)

    with codefile.open(
        encoding = "utf-8",
        mode = "a"
    ) as f:
        f.write(code)


    codefile = projectfolder_TEMP / f"{projectname}-fr.tex"
    code     = r"""
\documentclass[10pt, a4paper]{article}

\newcommand\thispack{\tdocpack{tns-functab}}

\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}

\usepackage{multicol}
\usepackage[inline]{enumitem}

\usepackage[french]{babel, varioref}
\frenchsetup{StandardItemLabels=true}

\usepackage[lang = french]{tutodoc}

\usepackage{amsmath}
\usepackage[locale=FR]{siunitx}
    """.strip() + f"""

% Package documented.
\\usepackage{{{projectname}}}
    """.rstrip() + '\n'*3

    for tmpfile in [
        ".tmp_fordoc.tex",
        ".tmp_thedoc.tex",
    ]:
        if not (projectfolder_TEMP / tmpfile).is_file():
            continue

        if tmpfile == ".tmp_thedoc.tex":
            code += r"""
\begin{document}

\title{Le package \texttt{tutodoc} - Documentation de type tutoriel}
\author{Christophe BAL}
\date{1\ier{} Janv. 2024 - Version 1.1.0}

\maketitle

\begin{abstract}
\noindent
Le paquet \thispack\ fournit des moyens intuitifs et efficaces pour taper des tableaux décrivant des fonctions mathématiques, ou bien des tableaux de données remplies éventuellement via des \tdocquote{fonctions informatiques}
\footnote{
	La référence à \tdocquote{fonction} est donc polysémique.
}.
Voici ce qui est actuellement proposé.
\begin{enumerate}
	\item Tableaux de données remplis à la main ou via une macro.

%	\item Tableaux de données pour des suites récursives remplis à la main et/ou via une macro.
%
%	\item Tableaux de signes et/ou de variations de fonctions réelles.
%
%	\item Tableaux de signes et/ou de variations associées à des courbes planes paramétrées réelles.
\end{enumerate}

\medskip

\noindent
Deux points importants à noter.
\begin{itemize}
    \item Sans le paquet \tdocpack{nicematrix} qui fait tout le travail ingrat, le paquet \thispack\ n'aurait certainement pas vu le jour.

    \item Cette documentation est aussi disponible en anglais.
\end{itemize}


% ------------------ %


\tdocsep

{\noindent
\small\itshape
\textbf{Abstract.}
The \thispack\ package provides intuitive and efficient ways of typing tables describing mathematical functions, or tables of data possibly filled in via \tdocquote{computer functions}
\footnote{
	The reference to \tdocquote{function} is therefore polysemous.
}.
Here is what is currently proposed.
\begin{enumerate}
	\item Data tables filled in by hand or via a macro.

%	\item Tables of data for recursive sequences filled in by hand and/or via a macro.
%
%	\item Tables of signs and/or variations of real functions.
%
%	\item Tables of signs and/or variations associated with real parametric plane curves.
\end{enumerate}

\medskip

\noindent
Two important points to note.
\begin{itemize}
    \item Without the \tdocpack{nicematrix} package which does all the thankless work, the \thispack\ package would certainly not have seen the light of day.

    \item This documentation is also available in French.
\end{itemize}
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

\tdocversion{1.0.0}[2024-01-01]

Première version publique du projet.

\end{document}
"""

    with codefile.open(
        encoding = "utf-8",
        mode = "a"
    ) as f:
        f.write(code)


    return projectfolder_TEMP
