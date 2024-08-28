from pathlib import Path
import              re


# ---------- #
# -- TAGS -- #
# ---------- #

TAG_LANG_EN = "en"
TAG_LOCALE  = "locale"

TAG_ABSTRACT = "abstract"

TAG_DIR  = "dir"
TAG_FILE = "file"

TAG_TOC  = "toc"

TAG_ABOUT_FILE = "about.yaml"

TAG_STY = "sty"
TAG_TEX = "tex"

TAG_RESRC     = "resource"
TAG_STY_RESRC = f"{TAG_STY}-{TAG_RESRC}"
TAG_TEX_RESRC = f"{TAG_TEX}-{TAG_RESRC}"

TAG_CFG_STY = "cfg.sty"
TAG_CFG_TEX = "cfg.tex"

TAG_ALL  = "all"
TAG_TEMP = "temp"

TAG_CREATION = "creation"
TAG_DATE     = "date"
TAG_DAY      = "day"
TAG_MONTH    = "month"
TAG_YEAR     = "year"

TAG_AUTHOR    = "author"
TAG_DESC      = "desc"
TAG_PROJ_DIR  = "proj-dir"
TAG_PROJ_NAME = "proj-name"
TAG_ROLLOUT   = "rollout"
TAG_SRC       = "source"
TAG_API       = "api"

TAG_VERSIONS = "versions"
TAG_NB       = "nb"
TAG_ALL      = "all"
TAG_LAST     = "last"

TAG_CONTRIB           = "contrib"
TAG_DOC               = "doc"
TAG_CHGE_LOG          = "changelog"
TAG_MANUAL            = "manual"
TAG_MANUAL_DEV_LANG   = "manual-dev-lang"
TAG_MANUAL_OTHER_LANG = "manual-other-lang"

TAG_STATUS          = "status"
TAG_STATUS_ON_HOLD  = "on hold"
TAG_STATUS_KO       = "ko"
TAG_STATUS_OK       = "ok"
TAG_STATUS_UPDATE   = "update"
TAG_STATUS_LANG_API = "lang-api"

TAG_TMP_STY_IMPORT  = '.tmp_pack_import.sty'
TAG_TMP_STY_OPTIONS = '.tmp_pack_options.sty'
TAG_TMP_STY_SRC     = '.tmp_pack_src.sty'

TAG_TMP_TEX_FOR_DOC = '.tmp_fordoc.tex'
TAG_TMP_TEX_THE_DOC = '.tmp_thedoc.tex'


TAG_TMP_PREAMBLE = 'preamble.cfg.tex'


# ------------------------- #
# -- MC = MAGIC COMMENTS -- #
# ------------------------- #

for kind in [
    "PACKAGES",
    "OPTIONS",
    "TOOLS",
    "FORDOC",
    "CONTRIB - LOAD",
]:
    varname = kind

    for old, new in [
        (' ', ''),
        ('-', '_')
    ]:
        varname = varname.replace(old, new)

    globals()[f"TAG_MC_{varname}"] = f"% == {kind} == %"


# -------------- #
# -- PATTERNS -- #
# -------------- #

CMDS_FOR_FILE_PATTERNS = [
    re.compile(
          r"^([^%\\]*)(.*)(\\"
        + macroname
        + ")(\[.*\][\t ]*\n?[\t ]*)?{(.*)}(.*)$"
    )
    for macroname in [
        "input",
        "tdoclatexshow",
        "tdoclatexinput",
        "tdocshowcaseinput",
        "tdocdocbasicinput",
    ]
]


CMD_ARG_PATTERN = re.compile('#(\d+)')


DATE_PATTERN = re.compile(r"==\n(\d+)\s+\((.+)\)\n==")


TITLE_PATTERNS = [
    re.compile(
          r"% ("
        + d
        + r"{2})\s+(.+)\s+("
        + d
        + r"{2}) %"
    )
    for d in "=-:"
]

# --------------- #
# -- LANGUAGES -- #
# --------------- #

LANG_NAMES = {
    'en' : {
        'en': "English",
        'fr': "French",
    },
    'fr' : {
        'en': "anglais",
        'fr': "français",
    },
}

HISTORY_TRANS = {
    'en' : "History",
    'fr' : "Historique",
}


# -------------- #
# -- SRC CODE -- #
# -------------- #

SRC_CODE_HEADER = """
This is file `<<PROJ_NAME>>.sty' generated automatically.

Copyright (C) <<CREATION_YEAR>>-<<LAST_YEAR>> by <<AUTHOR>>

This file may be distributed and/or modified under
the conditions of the GNU 3 License.
""".strip()


SRC_CODE_PROVIDE_PACK = """
\\ProvidesExplPackage
  {<<PROJ_NAME>>}
  {<<LAST_DATE>>}  % Creation: <<CREATION_DATE>>
  {<<LAST_NB_VER>>}
  {<<SHORT_DESC>>}
""".strip()
