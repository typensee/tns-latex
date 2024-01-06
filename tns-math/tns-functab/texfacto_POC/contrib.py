from .gather import *


def contrib_tex_template(text, localtools = ""):
    if localtools:
        localtools = f"""
% == FORDOC == %

{localtools}
"""


    return f"""
\\documentclass[12pt, a4paper]{{article}}

\\input{{../preamble.cfg.tex}}

{localtools}
\\begin{{document}}

{text}

\\end{{document}}
    """.lstrip()


def clean_main_tex(texfile):
    content     = texfile.read_text()
    new_content = []
    localtools  = []

    kind = ""

    for oneline in content.split('\n'):
        if kind == 'content':
            new_content.append(oneline)

        elif kind == 'tools':
            localtools.append(oneline)

        elif oneline.strip() == '\\begin{document}':
            kind = 'content'

        elif oneline.strip() == '% == FORDOC == %':
            kind = 'tools'

    new_content = '\n'.join(new_content)
    localtools  = '\n'.join(localtools)

    texfile.write_text(
        data = contrib_tex_template(
            text       = new_content,
            localtools = localtools
        )
    )


def update_contrib(
    projdir,
    toc_doc,
    toc_doc_resrces,
    main_lang = 'fr'
):
    contribdir = projdir / "contrib" / "doc" / "manual"
    srcdir     = projdir / "src"

# Update main doc.
    maindoc = contribdir / main_lang

    emptydir(maindoc)

    preambule = maindoc / "preamble.cfg.tex"

    copyfromto(
        srcdir  / "preamble.cfg.tex",
        preambule
    )

    preambule.write_text(
        data = f"""{preambule.read_text()}
\\usepackage[lang = french]{{tutodoc}}
"""
    )

    for docfile in toc_doc:
        copyfromto(
            srcdir  / docfile,
            maindoc / docfile
        )

        clean_main_tex(maindoc / docfile)


    copyfromto(
        srcdir  / "abstract" / "abstract.tex",
        maindoc / "abstract" / "abstract.tex"
    )

    clean_main_tex(maindoc / "abstract" / "abstract.tex")


    for resfile in toc_doc_resrces:
        copyfromto(
            resfile,
            maindoc / resfile.relative_to(srcdir)
        )


    for logfile in (srcdir / "changelog").glob("*/*/*.tex"):
        day   = logfile.name
        month = logfile.parent.name
        year  = logfile.parent.parent.name

        contrib_logfile = maindoc / "changelog" / year / f"{month}-{day}"

        copyfromto(
            logfile,
            contrib_logfile
        )

        contrib_logfile.write_text(
            data = contrib_tex_template(
                logfile.read_text(),
            )
        )


def add_contrib_doc(
    tmpdir,
    projdir,
    rolloutdir,
    toc_doc,
    main_lang = 'fr'
):
    projectname = projdir.name
    contribdir  = projdir / "contrib" / "doc" / "manual"

    for langdir in contribdir.glob("*"):
        if (
            not langdir.is_dir()
            or
            langdir.name.startswith('.')
            or
            langdir.name in ['changes', 'status', main_lang]
        ):
            continue

        lang = langdir.name

        print(f"+ MANUAL - New translation: {lang.upper()}.")

        destfile = rolloutdir / 'doc' / f'{projectname}-{lang}.tex'

        locale_tmpdir = tmpdir / f"{langdir.name}"

        emptydir(locale_tmpdir)

        for docpartfile in toc_doc:
            pieces = extractfrom_TEX(langdir / docpartfile)
            prepare_TEX(None, locale_tmpdir, *pieces)


        code = r"""
\documentclass[10pt, a4paper]{article}

\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}

\usepackage[english]{babel, varioref}

\usepackage{enumitem}

\usepackage{tabularray}
\usepackage{fmtcount}

\setlength{\parindent}{0em}
    """.strip() + f"""

% Package documented.
\\usepackage[lang = english]{{{projectname}}}
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
\date{\ordinalnum{1} Jan. 2024 - Version 1.1.0}

\maketitle

\begin{abstract}
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
\end{abstract}


\newpage
\tableofcontents
\newpage
"""

            with (locale_tmpdir / tmpfile).open(
                encoding = "utf-8",
                mode = "r"
            ) as f:
                code += f.read()

        code = code.strip()
        code += r"""
\section{History}

\tdocversion{1.1.0}[2024-01-06]

\begin{tdocnew}
	\item Change log : two new environments.
    \begin{enumerate}
        \item \tdocenv{tdocbreak} for breaking changes which are not backward compatible.

        \item \tdocenv{tdocprob} for identified problems.
    \end{enumerate}

	\item \tdocmacro{tdocinlatex}: a light yellow is used as the background color.
\end{tdocnew}

\tdocsep

\tdocversion{1.0.1}[2023-12-08]

\begin{tdocfix}
	\item \tdocmacro{tdocenv}: spacing is now correct, even if the \tdocpack{babel} package is not loaded with the French language.

	\item \tdocenv[{[nostripe]}]{tdocshowcase}: page breaks around \tdocquote{framing} lines should be rare from now on.
\end{tdocfix}

\tdocsep

\tdocversion{1.0.0}[2023-11-29]

First public version of the project.

\end{document}
    """

    codefile = locale_tmpdir.parent / f"{projectname}-en.tex"

    with codefile.open(
        encoding = "utf-8",
        mode = "a"
    ) as f:
        f.write(code)
