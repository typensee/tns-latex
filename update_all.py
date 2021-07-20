#!/usr/bin/env python3

from datetime import datetime

from tool.tnsfactory.src import *


# --------------- #
# -- CONSTANTS -- #
# --------------- #

MONOREPO_DIR = PPath(__file__).parent
LOG_FILE     = MONOREPO_DIR / "x-log-x.txt" 

# New log file.
timestamp = lambda: datetime.now().strftime("%Y-%m-%d (%H:%M:%S)")

LOG_FILE.touch()

with LOG_FILE.open(
    encoding = "utf8",
    mode     = "w"
 ) as logfile:
    title = f'LOG FILE - MONOREPO "{MONOREPO_DIR.name}"'
    deco  = "="*len(title)
    
    logfile.write(
f"""
{deco}
{title}
{deco}

STARTING TIME STAMP: {timestamp()}
""".lstrip())


# ----------- #
# -- TOOLS -- #
# ----------- #

MAIN_STEPS = Step()

DECO_STEPS = [c for c in "*+"]

for i, deco in enumerate(DECO_STEPS, 1):
    exec(
        f'SUB_{i}_STEPS = Step(textit = lambda n, t: " "*4*{i} + f"{deco} {{t}}")'
    )


# -------------------------- #
# -- FINDING THE PACKAGES -- #
# -------------------------- #

NL()
ASCII_FRAME("TNSLATEX - STARTING THE ANALYSIS")

NL()
MAIN_STEPS("Looking for packages to build or update.")

allpacks        = packdirs(MONOREPO_DIR)
packs_to_update = packschanged(MONOREPO_DIR, allpacks)

if allpacks:
    percentage = len(packs_to_update)/len(allpacks)*100
else:
    percentage = 0

SUB_1_STEPS(
    f"Total number of packages        = {len(allpacks)}"
)
SUB_1_STEPS(
    f"Number of packages with changes = {len(packs_to_update)}"
    f"  -->  {percentage:.2f}%"
)


# ------------------------- #
# -- UPDATE EACH PACKAGE -- #
# ------------------------- #

pbfound = []

if not packs_to_update:
    NL()
    MAIN_STEPS("No changes found.")

else:
    for packchged in packs_to_update:
        NL()
        MAIN_STEPS(f'Working on "{packchged - MONOREPO_DIR}".')

        updater = UpdateOnePack(
            monorepo   = MONOREPO_DIR,
            dirpath    = packchged, 
            stepprints = [SUB_1_STEPS, SUB_2_STEPS],
            logfile    = LOG_FILE,
            kindwanted = TOC.KIND_DIR
        )
        updater.build()

        if updater.success:
            SUB_1_STEPS("OK.")
        
        else:
            pbfound.append(updater.dir_relpath)
            SUB_1_STEPS(f'PROBLEM with "{updater.dir_relpath}".')

    NL()
    MAIN_STEPS("All changes have been treated.")


# --------------- #
# -- PB FOUND? -- #
# --------------- #

if pbfound:
    plurial = "" if len(pbfound) == 1 else "s"

    NL(2)
    ASCII_FRAME(f"{len(pbfound)} PB{plurial} FOUND")

    NL()
    SUB_1_STEPS(
        f'Look at "{MONOREPO_DIR.name}/{LOG_FILE - MONOREPO_DIR}"'
    )

    if plurial:
        SUB_1_STEPS('List of problematic packages.')

    else:
        SUB_1_STEPS('Just one problematic package.')

    for pbpack in pbfound:
        SUB_2_STEPS(pbpack)


# ------------------------ #
# -- NOTHING ELSE TO DO -- #
# ------------------------ #

with LOG_FILE.open(
    encoding = "utf8",
    mode     = "a"
 ) as logfile:
    logfile.write("\n"*2)
    logfile.write(f"ENDING TIME STAMP: {timestamp()}")

NL(2)
ASCII_FRAME("TNSLATEX - ANALYSIS FINISHED")
NL()
