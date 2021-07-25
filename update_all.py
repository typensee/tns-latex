#!/usr/bin/env python3

from datetime import datetime

from tnstools.tnsfactory.src import *


# ----------- #
# -- TOOLS -- #
# ----------- #

INIT_MONOREPO = True
# INIT_MONOREPO = False

LANGS_SUPPORTED = ["FR"]


# ----------- #
# -- TOOLS -- #
# ----------- #

def tologfile(
    lines: List[str],
    mode : str = "a"
) -> None:
    global LOG_FILE

    with LOG_FILE.open(
        encoding = "utf8",
        mode     = mode
    ) as logfile:
        for oneline in lines:
            logfile.write(oneline)
            logfile.write("\n")


def timestamp(kind: str) -> None:
    now = datetime.now().strftime("%Y-%m-%d (%H:%M:%S)")

    timeTXT = f"{kind} TIME STAMP: {now}"

    tologfile([
        "",
        ASCII_FRAME_2(timeTXT)
    ]) 

# --------------- #
# -- CONSTANTS -- #
# --------------- #

MONOREPO_DIR = PPath(__file__).parent
LOG_FILE     = MONOREPO_DIR / "x-log-x.txt" 

# New log file.
LOG_FILE.touch()

title = f'LOG FILE - MONOREPO "{MONOREPO_DIR.name}"'
deco  = "="*len(title)

tologfile(
    mode  = "w", # We want to erase a potential existing content.
    lines = [
        deco,
        title,
        deco,
    ]
)

timestamp("STARTING")


# -------------------------- #
# -- FINDING THE PACKAGES -- #
# -------------------------- #

NL()
print(ASCII_FRAME_1("TNSLATEX - STARTING THE ANALYSIS"))

NL()
MAIN_STEPS("Looking for packages to build or update.")

allpacks = packdirs(MONOREPO_DIR)

if not allpacks:
    packs_to_update = []

    SUB_1_STEPS("No packages found.")

else:
    SUB_1_STEPS(f"Total number of packages = {len(allpacks)}")

    if INIT_MONOREPO:
        SUB_1_STEPS(f"Initialize the monorepo: all packages treated.")

        packs_to_update = allpacks

    else:
        SUB_1_STEPS('Using "git a".')

        packs_to_update = packschanged(MONOREPO_DIR, allpacks)

        percentage = len(packs_to_update) / len(allpacks) * 100

        SUB_1_STEPS(
            f"Number of packages changed = {len(packs_to_update)}"
            f"  -->  {percentage:.2f}%"
        )


# ------------------------- #
# -- UPDATE EACH PACKAGE -- #
# ------------------------- #

pbfound = []

# Empty monorepo...
if not allpacks:
    ...

# No pack to update.
elif not packs_to_update:
    NL()
    MAIN_STEPS("No changes found.")

# Some pack to update.
else:
    for packchged in packs_to_update:
        NL()
        MAIN_STEPS(f'{MESSAGE_WORKING} inside "{packchged - MONOREPO_DIR}".')

        updater = UpdateOnePack(
            monorepo   = MONOREPO_DIR,
            dirpath    = packchged, 
            stepprints = [SUB_1_STEPS, SUB_2_STEPS],
            logfile    = LOG_FILE
        )
        updater.build()

        NL()

        if updater.success:
            SUB_1_STEPS(f'OK for "{updater.dir_relpath}".')
        
        elif updater.problems.errorfound():
            plurial = "S" if updater.problems.several_errors else ""
            
            SUB_1_STEPS(
                f'{MESSAGE_ERROR}{plurial} with "{updater.dir_relpath}".'
            )

    NL()
    MAIN_STEPS("All changes have been treated.")


# --------------- #
# -- PB FOUND? -- #
# --------------- #

if updater.problems.pbfound():
    updater.problems.resume()

else:
    title = f"NO {MESSAGE_WRONG_SRC} FOUND."

    tologfile([
        "",
        ASCII_FRAME_2(title)
    ]) 


# ------------------------ #
# -- NOTHING ELSE TO DO -- #
# ------------------------ #

timestamp("ENDING")

NL(2)
print(ASCII_FRAME_1("TNSLATEX - ANALYSIS FINISHED"))
NL()
