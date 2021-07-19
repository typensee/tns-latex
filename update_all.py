#!/usr/bin/env python3

from tool.tnsfactory.src import *


# ----------------- #
# -- DEV. "TEST" -- #
# ----------------- #

if __name__ == "__main__":
    projectdir = PPath(__file__).parent

    allpacks = packdirs(projectdir)

    print(allpacks)

    