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
