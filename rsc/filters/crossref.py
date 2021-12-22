from collections import defaultdict
from string import ascii_lowercase
import textwrap
import sys

from panflute import Header
from panflute import Link
from panflute import Str
from panflute import RawInline
from panflute import Cite
from panflute import Para
from panflute import Table
from panflute import Caption
from panflute import Space
from panflute import Image
from panflute import Strong
from panflute import run_filters
import numpy as np

import logging


#logging.basicConfig(filename="crossref.txt", filemode="w")
#logger = logging.getLogger()

TABLE_IDENTIFIER = "tbl:"
FIGURE_IDENTIFIER = "fig:"
SECTION_IDENTIFIER = "sec:"
APPENDIX_IDENTIFIER = "ap:"


LATEX_SECTION_MAPPER = {
    1: r"\section",
    2: r"\subsection",
    3: r"\subsubsection",
}


def appendix_letters(n):
    n_letters = (n // 26) + 1
    ith_letter = (n % 26) - 1
    return (ascii_lowercase[ith_letter] * n_letters).upper()


def find_section(elem):
    if isinstance(elem, Header):
        logger.exception("ANC2 %s", elem.identifier)
        return elem.identifier

    i = -1
    logger.exception("FIND SECTION FOR %s", elem)
    logger.exception("FIRST OFFSET %s", elem.ancestor(2))
    while elem.offset(i):
        ancestor = elem.offset(i)
        logger.exception("ANC: %s", ancestor)
        if isinstance(ancestor, Header):
            return ancestor.identifier
        i -= 1


def in_appendix(elem):
    if hasattr(elem, "classes") and ("appendix" in elem.classes):
        return True

    i = 1
    while elem.ancestor(i):
        ancestor = elem.ancestor(i)
        classes = getattr(ancestor, "classes", [])
        if "appendix" in classes:
            return True
        i += 1

    return False


class SectionReference:
    def __init__(self) -> None:
        self.sections = dict()
        self.section_counter = np.zeros(len(LATEX_SECTION_MAPPER.keys()), dtype=np.int8)

        self.appendix = dict()
        self.appendix_counter = np.zeros(
            len(LATEX_SECTION_MAPPER.keys()), dtype=np.int8
        )

        self.latest_insert = None

    def add_section(self, id_: str, level: int, type_: str) -> None:
        _level_ix = level - 1

        if type_ == "section":
            self.section_counter[_level_ix] += 1
            self.section_counter[level:] = 0
            self.sections[id_] = list(self.section_counter)
        elif type_ == "appendix":
            self.appendix_counter[_level_ix] += 1
            self.section_counter[level:] = 0
            self.appendix[id_] = list(self.appendix_counter)

        self.latest_insert = id_

    def find_section(self, id_: str) -> list[int]:
        if id_ in self.sections:
            number = self.sections[id_]
            return ".".join(str(n) for n in number if n > 0)

        elif id_ in self.appendix:
            number = self.appendix[id_]
            literal = appendix_letters(number[0])
            numbers = ".".join(str(n) for n in number[1:] if n > 0)
            return ".".join((literal, numbers)).rstrip(".")

    def __str__(self) -> str:
        sections = ", ".join(
            [": ".join((ref, self.find_section(ref))) for ref in self.sections]
        )
        appendices = ", ".join(
            [": ".join((ref, self.find_section(ref))) for ref in self.appendix]
        )
        return textwrap.dedent(
            f"""
        SectionReference(
            sections=[{sections}]

            appendices=[{appendices}]
            )"""
        )


SECTIONS = SectionReference()


class GenericReference:
    def __init__(self, type_: str) -> None:
        self.type_ = type_
        self.items = dict()
        self.items_counter = 0

        self.appendix_items = dict()
        self.appendix_counter = defaultdict(int)

    def add_item(self, elem) -> None:

        id_ = elem.identifier

        if in_appendix(elem):
            type_ = "appendix"
        else:
            type_ = "main"

        if any(id_ in i for i in (self.items, self.appendix_items)):
            print(f"ERROR: Duplicate cite-key: {id_} in\n{self}", file=sys.stderr, flush=True)

        if type_ == "main":
            self.items_counter += 1
            self.items[id_] = self.items_counter
        elif type_ == "appendix":
            latest_insert = SECTIONS.find_section(SECTIONS.latest_insert)
            if latest_insert:
                literal = latest_insert[0]
            else:
                print(f"ERROR: Appendix Section could not be found - {SECTIONS.latest_insert}", file=sys.stderr, flush=True)
                return "?"
            self.appendix_counter[literal] += 1
            self.appendix_items[id_] = "".join(
                (literal, str(self.appendix_counter[literal]))
            )

    def find_item(self, id_):
        global SECTIONS
        if id_ in self.items:
            return str(self.items[id_])
        elif id_ in self.appendix_items:
            return self.appendix_items[id_]

    def __str__(self) -> str:
        items = ", ".join(
            [": ".join((ref, str(self.items[ref]))) for ref in self.items]
        )
        appendix_items = ", ".join(
            [
                ": ".join((ref, str(self.appendix_items[ref])))
                for ref in self.appendix_items
            ]
        )
        return textwrap.dedent(
            f"""
        {self.type_}Reference(
            items=[{items}]

            appendix_items=[{appendix_items}]
            )"""
        )


FIGURES = GenericReference(type_="Figures")
TABLES = GenericReference(type_="Tables")


def _process_item(elem, doc, reference):
    id_ = elem.citations[0].id
    text = reference.find_item(id_)
    if text is None:
        text = Strong(Str(f"?{id_}"))
        print(f"ERROR: Ref {id_} not defined", file=sys.stderr, flush=True)
    else:
        text = Str(text)
    url = f"#{id_}"
    link = Link(url=url, title=str(text))
    link.content = [text]
    return link


def _process_section(elem, doc):
    global SECTIONS
    id_ = elem.citations[0].id

    if doc.format == "latex":
        return RawInline(f"\\ref{{{id_}}}", format="tex")
    elif doc.format == "docx":
        link = SECTIONS.find_section(id_)
        logger.exception("PROC SEC: %s <--> %s", id_, link)
        return Str(link)


def replace_links(elem, doc):
    global TABLES
    global FIGURES
    if isinstance(elem, Cite) and len(elem.citations) == 1:
        cite = elem.citations[0]
        key = cite.id
        if key.startswith(TABLE_IDENTIFIER):
            elem = _process_item(elem, doc, TABLES)
        elif key.startswith(FIGURE_IDENTIFIER):
            elem = _process_item(elem, doc, FIGURES)
        elif key.startswith(SECTION_IDENTIFIER):
            elem = _process_section(elem, doc)
        elif key.startswith(APPENDIX_IDENTIFIER):
            elem = _process_section(elem, doc)

    return elem


def set_targets(elem, doc):
    global SECTIONS
    global FIGURES
    global TABLES

    if isinstance(elem, Header):
        if "unnumbered" in elem.classes:
            return elem
        level = elem.level
        id_ = elem.identifier

        if level > 3:
            raise Exception("Do not use Headers with level > 3")

        if in_appendix(elem):
            type_ = "appendix"
        else:
            type_ = "section"

        SECTIONS.add_section(id_, level, type_)

        if doc.format == "latex":
            section = LATEX_SECTION_MAPPER[level]
            content = Para(
                RawInline(f"{section}{{", format="tex"),
                *elem.content,
                RawInline(f"}}~\\label{{{id_}}}", format="tex"),
            )
            return content

        if doc.format == "docx":
            elem.content = [
                Str(SECTIONS.find_section(elem.identifier)),
                Space,
                Space,
                *elem.content,
            ]
            return elem

    elif isinstance(elem, Image):
        FIGURES.add_item(elem)

    elif isinstance(elem, Table):
        TABLES.add_item(elem)
        
        if doc.format == "latex":
            try:
                para = elem.caption.content[0]
            except IndexError:
                para = Para()
            caption = para.content
            ref = RawInline(f"\\protect\\hypertarget{{{elem.identifier}}}{{}}", format="tex")
            elem.caption = Caption(Para(*caption, ref))

        return elem
        



def set_table_targets(elem, doc):
    if isinstance(elem, Table):

        identifier = elem.identifier

        if doc.format == "latex":
            elem.caption = Caption(
                Para(
                    *elem.caption.content[0].content,
                    RawInline(
                        f"\\hypertarget{{{identifier}}}{{}}",
                        format="latex",
                    ),
                )
            )
    return elem


def main(doc=None):
    return run_filters(
        [set_targets, replace_links]
    )


if __name__ == "__main__":
    main()
