#!/usr/bin/python3
from panflute import Div
from panflute import RawBlock, RawInline
import textwrap
from panflute import run_filters
from panflute.elements import Header

import logging

#logging.basicConfig(filename="appendix.txt", filemode="w")
#logger = logging.getLogger()


def in_appendix(elem):
    if hasattr(elem, "classes") and ("appendix" in elem.classes):
        return True
    i = 1
    while elem.ancestor(i):
        ancestor = elem.ancestor(i)
        if hasattr(ancestor, "classes") and ("appendix" in ancestor.classes):
            return True
        i += 1

    return False


def define_appendix(elem, doc):

    if not doc.format == "latex":
        return None

    if not isinstance(elem, Div):
        return elem

    if in_appendix(elem):
        elem.content = [
            RawBlock(r"\begin{appendix}", format="latex"),
            RawBlock(
                textwrap.dedent(
                    r"""
                    \setcounter{table}{0}
                    \renewcommand{\thetable}{\Alph{section}\arabic{table}}
                    """
                ),
                format="latex",
            ),
            *elem.content,
            RawBlock(r"\end{appendix}", format="latex"),
        ]
        return elem


def reset_tablecounter(elem, doc):
    if not isinstance(elem, Header):
        return elem
    if elem.level != 1:
        return elem
    if in_appendix(elem):
        elem = [RawBlock(r"\setcounter{table}{0}", format="latex"), elem]
    return elem


def main(doc=None):
    return run_filters([define_appendix, reset_tablecounter], doc=doc)


if __name__ == "__main__":
    main()
