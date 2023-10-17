#!/bin/bash

THIS_DIR="$(cd "$(dirname "$0")" && pwd)"

# latexdef -l -p amsmath

# We want to break on newline rather on spacing characrters.
IFS=$'\n'

for infos in $(tlmgr list --only-installed)
do
    name=${infos#i } # Remove everything up to a colon and space
    name=${name%:*}              # Remove the M at the end

    echo " --> $name"

    found="$(latexdef -l -p "$name")"

   # echo "$found"
done
