#!/usr/bin/env python3

from datetime import datetime

# ---------------- #
# -- TIME STAMP -- #
# ---------------- #

###
# prototype::
#     speaker = speaker.Speaker ;  
#               the class used to speak on the terminal and in the log file.
#     kind    = ; # See Python typing...
#               the kind of time stamp ("START" and "END" for us).
###
def timestamp(
    speaker, # Can't use the type speaker.Speaker.
    kind: str
) -> None:
    now = datetime.now().strftime("%Y-%m-%d (%H:%M:%S)")

    timeTXT = f"{kind} TIME STAMP: {now}"

    speaker.title(
        title = timeTXT,
        level = 2
    )
