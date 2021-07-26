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
        
        else:
            plurial = "S" if updater.problems.several_errors else ""
            
            SUB_1_STEPS(
                f'{MESSAGE_ERROR}{plurial} with "{updater.dir_relpath}".'
            )

    NL()
    MAIN_STEPS("All changes have been treated.")


# --------------- #
# -- PB FOUND? -- #
# --------------- #

if not updater.success:
    updater.problems.resume()

else:
    title = f"NO {MESSAGE_WRONG_SRC} FOUND."

    tologfile([
        "",
        ASCII_FRAME_2(title)
    ]) 
