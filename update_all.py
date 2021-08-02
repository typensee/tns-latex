        if updater.success:
            SUB_1_STEPS(f'OK for "{updater.dir_relpath}".')
        
        else:
            plurial = "S" if updater.problems.several_errors else ""
            
            SUB_1_STEPS(
                f'{MESSAGE_ERROR}{plurial} with "{updater.dir_relpath}".'
            )

    NL()
    MAIN_STEPS("All changes have been treated.")
