#! /usr/bin/env python3

from abc import ABCMeta, abstractmethod


# --------------- #
# -- CONSTANTS -- #
# --------------- #

# -- INTERFACE - AUTO CODE - START -- #

CONTEXT_CRITICAL = "critical"
CONTEXT_ERROR    = "error"
CONTEXT_GOOD     = "good"
CONTEXT_NORMAL   = "normal"
CONTEXT_WARNING  = "warning"

ALL_CONTEXTS = [
    CONTEXT_CRITICAL,
    CONTEXT_ERROR,
    CONTEXT_GOOD,
    CONTEXT_NORMAL,
    CONTEXT_WARNING
]

# -- INTERFACE - AUTO CODE - END -- #

GLOBAL_STYLE_BW    = "balck & white"
GLOBAL_STYLE_COLOR = "color"

ALL_GLOBAL_STYLES = [
    GLOBAL_STYLE_BW,
    GLOBAL_STYLE_COLOR,
]


# -------------------------------- #
# -- ABSTRACT / INTERFACE CLASS -- #
# -------------------------------- #

###
# This abtract/interface class defines the common ¨api of the speakers.
###

class AbstractSpeaker(metaclass=ABCMeta):
# Source to have a real interface: 
#     * https://realpython.com/python-interface/#using-abcabcmeta 
    @classmethod
    def __subclasshook__(cls, subclass) -> None:
        goodinterface = all(
            hasattr(subclass, methodname) and 
            callable(getattr(subclass, methodname)) 
            for methodname in [
                'print',
                'NL',
            ]
        )

        return goodinterface

###
# prototype::
#     style    = _ in ALL_GLOBAL_STYLES; // See Python typing...
#                a global style for the output. Internally this style is  
#                stored in the attribut ``global_style``.
#     maxwidth = ; // See Python typing...
#                the maw width expected for hard wrapped contents.
###
    def __init__(
        self,
        style   : str,
        maxwidth: int = 80
    ) -> None:
        assert(style in ALL_GLOBAL_STYLES)

        self.maxwidth     = maxwidth
        self.global_style = style


###
# prototype::
#     text = ; // See Python typing...
#            a text to add as it.
###
    @abstractmethod
    def print(self, text: str,) -> None:
        raise NotImplementedError

###
# prototype::
#     repeat = (1) ; // See Python typing...
#              the numebr of empty lines wanted.
###
    @abstractmethod
    def NL(self, repeat: int = 1) -> None:
        raise NotImplementedError


###
# prototype::
#     context = _ in ALL_CONTEXTS (CONTEXT_NORMAL) ; // See Python typing...
#               a context for formatting ¨infos.
#
#
# info::
#     This method doesn't need to be implemented (some speaker has no style 
#     like the log like ones).
###
    def style(self, context: str = CONTEXT_NORMAL) -> None:
# Help for debuging.
#         print(self.__class__)
        ...


###
# prototype::
#     text = ; // See Python typing...
#            a text to be hard wrapped.
#     tab  = (""); // See Python typing...
#            a possible tabulation to use for each new line created.
#
#     :return: = ; // See Python typing...
#                a wrapped message of maximal width ``self.maxwidth``.
###
    def hardwrap(
        self,
        text: str,
        tab : str = ""
    ) -> str:
        shortlines = []

        for oneline in text.split('\n'):
            words = [w.strip() for w in oneline.split(' ')]

            if shortlines:
                lastline = tab
            
            else:
                lastline = ""

            lastline += words.pop(0)


            while(words):
                oneword = words.pop(0)

                len_lastline = len(lastline)
                len_word     = len(oneword)

                if len_lastline + len_word >= self.maxwidth :
                    shortlines.append(lastline)
                    lastline = tab

                else:
                    lastline += " "
                    
                lastline += oneword

            shortlines.append(lastline)

        return "\n".join(shortlines)
