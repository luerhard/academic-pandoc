from collections import defaultdict
from string import ascii_lowercase

from panflute import Div, Space, Header, run_filters, Str, Link


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


def replace_headers(elem, doc):
    if isinstance(elem, Div) and elem.identifier == "beginappendix":
        doc.in_appendix = True
    elif isinstance(elem, Div) and elem.identifier == "endappendix":
        doc.in_appendix = False
    if isinstance(elem, Header):
        if "unnumbered" not in elem.classes:
            header_level = get_current_level(doc, elem.level)
            if doc.in_appendix:
                doc.appendix_headers["#" + elem.identifier] = header_level

            title = [Str(header_level), Space, Space, *elem.content]
            elem.content = title
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
