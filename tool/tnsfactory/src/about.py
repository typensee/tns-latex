#! /usr/bin/env python3

from .common import *


# ----------- #
# -- TOOLS -- #
# ----------- #

###
# This class extracts ¨infos from the ``about.peuf`` file of a package.
###

class About:
###
# prototype::
#     anadir = common.AnaDir ;  
#              any class having the ¨api of ``common.AnaDir``.
###
    def __init__(
        self,
        anadir# Can't use the type common.AnaDir (cyclic imports).
    ) -> None:
        self.anadir = anadir

###
# This method extracts ¨infos from the ``about.peuf`` file of the pcakage 
# if it is possible.
###
    def build(self) -> None:
# Nothing found... for the moment.
        self.anadir.about = None

# File exists?
        aboutpath = self.anadir.dirpath / ABOUT_NAME

        if not aboutpath.is_file():
            if self.anadir.needabout:
                self.anadir.error(MESSAGE_ABOUT + "no file found but required.")

            return

# Good peuf structure?
        try:
            with ReadBlock(
                content = aboutpath,
                mode    = ABOUT_PEUF_MODE
            ) as datas:
                about = datas.mydict("std nosep nonb")

        except PeufError as e:
            self.anadir.error(MESSAGE_ABOUT + "illegal file.")
            return

# Good keys for the ``general`` block?
        if GENE_TAG in about:
            pbfound        = False
            gene_keys_used = set(about[GENE_TAG].keys())

            for kind, set_1, set_2 in [
                ("missing", GENE_ALL_TAGS , gene_keys_used),
                ("extra"  , gene_keys_used, GENE_ALL_TAGS ),
            ]:
                pbkeys = set_1 - set_2

                if pbkeys:
# Missing + extra ?
                    tab = " "*2 if pbfound else ""

                    pbfound = True
                    plurial = "" if len(pbkeys) == 1 else "s"

                    pbkeys = [f"'{k}'" for k in pbkeys]
                    pbkeys.sort()
                    pbkeys = ", ".join(pbkeys)

                    self.anadir.error(
                        MESSAGE_ABOUT
                        + f"{kind.title()} key{plurial} {tab}-> "
                        + f"{pbkeys}."
                    )

# Everything seems ok.
        self.anadir.about = about
