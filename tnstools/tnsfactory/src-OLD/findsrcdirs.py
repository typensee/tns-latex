# Some dirs found.
    if paths:
        plurial = "" if len(paths) == 1 else "s"
        
        anadir.stepprints[0](
            f"{MESSAGE_SRC}: {len(paths)} {kind}{plurial} from {methodused}."
        )

# Nothing more to do.
    return paths
