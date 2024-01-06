# --------------- #
# -- CONSTANTS -- #
# --------------- #

CHANGELOGNEXT="changelog/next.tex"

THISDIR=$(dirname "$0")
WORKINGDIR=$(pwd)


# ----------------------- #
# -- ONE FOLDER NEEDED -- #
# ----------------------- #

if [ -z "$1" ]
then
    echo "CRITICAL - Missing arg: absolute target folder needed."
    exit 1
fi

if [ ! $# -eq 1 ]
then
    echo "CRITICAL - Too much arguments!"
    exit 1
fi

TARGET=$1

if [ ! -d "$TARGET" ]
then
    echo "CRITICAL - Missing folder: ''$TARGET''."
    exit 1
fi


# --------------------- #
# -- LISTED PROJECTS -- #
# --------------------- #

function nocompile {
    open "$1"
}

cd "$TARGET"

for f in */*.tex
do
    fdir=$(dirname "$f")

    if [ "$f" != "$CHANGELOGNEXT" ]
    then
        cd "$TARGET/$fdir"

        echo "-- NEW TEX FILE --"
        echo "$f"
        echo ""
        SOURCE_DATE_EPOCH=0 FORCE_SOURCE_DATE=1 latexmk -quiet -pdf -pdflatex="pdflatex --interaction=nonstopmode --halt-on-error --shell-escape  %O %S" "$TARGET/$f" || nocompile "$TARGET/$f"

        # latexmk -c "$TARGET/$f"
    fi
done # for f in */*.tex;
