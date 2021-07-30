#! /usr/bin/env python3


import re

from mistool.os_use   import DIR_TAG, FILE_TAG



# ------------- #
# -- SOURCES -- #
# ------------- #


# -------------- #
# -- MESSAGES -- #
# -------------- #

LOG_ID, TERM_ID = range(2)

MESSAGE_WORKING = "Working"

MESSAGE_TEMPLATE_FILE = lambda name: f"``{name}`` file -> "

MESSAGE_ABOUT      = MESSAGE_TEMPLATE_FILE(ABOUT_NAME)
MESSAGE_SRC_ABOUT  = MESSAGE_TEMPLATE_FILE(f"{SRC_DIR_NAME}/{ABOUT_NAME}")
MESSAGE_SRC        = "Source"
MESSAGE_FINAL_PROD = "Final Product"

MESSAGE_WRONG_SRC = "BAD SOURCE"


