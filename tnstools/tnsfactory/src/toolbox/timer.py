#!/usr/bin/env python3

from datetime import datetime

from .speaker import *


# ---------------- #
# -- TIME STAMP -- #
# ---------------- #

###
# prototype::
#     speaker = speaker.allinone.Speaker ;  
#               the class used to speak on the terminal and in the log file.
#     kind    = ; // See Python typing...
#               the kind of time stamp ("START" and "END" for us).
#     with_NL = (True); // See Python typing...
#               ``True`` asks to add a new line after the title and
#               ``False`` to not do this 
###

def timestamp(
    speaker: Speaker,
    kind   : str,
    with_NL: bool = True,
) -> None:
    now = datetime.now().strftime("%Y-%m-%d (%H:%M:%S)")

    timeTXT = f"{kind} TIME STAMP: {now}"

    speaker.recipe(
        FORLOG,
            {VAR_TITLE  : timeTXT, 
             VAR_LEVEL  : 2, 
             VAR_WITH_NL: with_NL},
    )
