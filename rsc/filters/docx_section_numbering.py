from collections import defaultdict
from os import access
from string import ascii_lowercase

from panflute import Div, Space, Header, run_filters, Str, Link, Table

import logging

logging.basicConfig(filename="numbering.txt", filemode="w")
logger = logging.getLogger()


def prepare(doc):
    doc.in_appendix = False
    doc.section_levels = []
    doc.appendix_levels = []
    doc.appendix_headers = defaultdict(str)
    return doc


def appendix_letters(n):
    n_letters = (n // 26) + 1
    ith_letter = (n % 26) - 1
    return (ascii_lowercase[ith_letter] * n_letters).upper()


def get_current_level(doc, level):
    index = level - 1

    if doc.in_appendix:

        levels = getattr(doc, "appendix_levels")
    else:
        levels = getattr(doc, "section_levels")

    try:
        levels[index] += 1
    except IndexError:
        levels.append(1)

    levels[level:] = [0] * (len(levels) - level)

    if doc.in_appendix:
        letters = appendix_letters(levels[0])
        if len(levels) == 1:
            return letters
        else:
            out = [letters] + [str(i) for i in levels[1:level]]
            return ".".join(out)
    return ".".join(str(i) for i in levels[:level])


def in_appendix(elem):
    if hasattr(elem, "classes") and ("appendix" in elem.classes):
        return True

    i = 1
    while elem.ancestor(i):
        ancestor = elem.ancestor(i)
        classes = getattr(ancestor, "classes", [])
        logger.error("%s - %s", getattr(ancestor, "identifier", None), classes)
        if "appendix" in classes:
            return True
        i += 1

    return False


def replace_headers(elem, doc):

    if in_appendix(elem):
        doc.in_appendix = True
    else:
        doc.in_appendix = False
    if isinstance(elem, Header):
        if "unnumbered" not in elem.classes:
            if doc.format == "doc":
                header_level = get_current_level(doc, elem.level)
                if in_appendix(elem):
                    doc.appendix_headers["#" + elem.identifier] = header_level

                if doc.format == "doc":
                    title = [Str(header_level), Space, Space, *elem.content]
                    elem.content = title
                elif doc.format == "latex":
                    pass

                return elem
        else:
            return elem


def replace_links(elem, doc):
    if isinstance(elem, Link) and elem.url in doc.appendix_headers:
        elem.content = [Str(doc.appendix_headers[elem.url])]
        return elem


def main(doc=None):
    return run_filters([replace_headers, replace_links], prepare=prepare, doc=doc)


if __name__ == "__main__":
    main()
