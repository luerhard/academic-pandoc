from collections import defaultdict
from string import ascii_lowercase
import textwrap
import sys

from typing import List

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
from panflute import Plain
from panflute import run_filters
import numpy as np

# for debugging uncomment and use logger.
# import logging
# logging.basicConfig(filename="crossref.txt", filemode="w")
# logger = logging.getLogger()

# Set valid identifiers for links in your Markdown document
TABLE_IDENTIFIER = "tbl:"
FIGURE_IDENTIFIER = "fig:"
SECTION_IDENTIFIER = "sec:"
APPENDIX_IDENTIFIER = "ap:"


# Set Prefix in Figure Captions
def FIGURE_PREFIX(fign):
    return Str(f"Figure {fign}: ")


# Set Prefix in Table Captions
def TABLE_PREFIX(fign):
    return Str(f"Table {fign}: ")


LATEX_SECTION_MAPPER = {
    1: r"\section",
    2: r"\subsection",
    3: r"\subsubsection",
    4: r"\paragraph",
    5: r"\subparagraph",
}


def appendix_letters(n):
    n_letters = (n // 26) + 1
    ith_letter = (n % 26) - 1
    return (ascii_lowercase[ith_letter] * n_letters).upper()


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

    def find_section(self, id_: str) -> List[int]:
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
            f"""SectionReference(sections=[{sections}]
            appendices=[{appendices}])"""
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
        if in_appendix(elem):
            type_ = "appendix"
        else:
            type_ = "main"

        id_ = elem.identifier

        if any(id_ in i for i in (self.items, self.appendix_items)):
            print(
                f"ERROR: Duplicate cite-key: {id_} in\n{self}",
                file=sys.stderr,
                flush=True,
            )

        if type_ == "main":
            self.items_counter += 1
            if not elem.identifier:
                elem.identifier = f"{self.type_}-{self.items_counter}"
                id_ = elem.identifier
            self.items[id_] = self.items_counter
        elif type_ == "appendix":
            latest_insert = SECTIONS.find_section(SECTIONS.latest_insert)
            if latest_insert:
                literal = latest_insert[0]
            else:
                print(
                    f"ERROR: Appendix Section could not be found - {SECTIONS.latest_insert}",
                    file=sys.stderr,
                    flush=True,
                )
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
            f"""{self.type_}Reference(items=[{items}]
            appendix_items=[{appendix_items}])"""
        )


FIGURES = GenericReference(type_="figure")
TABLES = GenericReference(type_="table")


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
    link = SECTIONS.find_section(id_)
    if not link:
        bad_reference = Strong(Str(f"?{id_}"))
        print(
            f"ERROR: bad reference. {id_} not found.",
            file=sys.stderr,
            flush=True,
        )

    if doc.format == "latex":
        if not link:
            return bad_reference
        return RawInline(f"\\ref{{{id_}}}", format="tex")
    elif doc.format == "docx":
        if not link:
            return bad_reference
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
        
        if level > 5:
            raise Exception("Do not use Headers with level > 5")

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
                RawInline(f"}}\\label{{{id_}}}", format="tex"),
            )
            return content

        if doc.format == "docx":
            if level <= 3:
                elem.content = [
                    Str(SECTIONS.find_section(elem.identifier)),
                    Space,
                    Space,
                    *elem.content,
                ]
            elif level == 4:
                # handle unnumbered header 4 sections
                elem.content = [
                    *elem.content,
                ]
            else:
                # handle inline paragraph sections (header 5)
                merged = elem.next
                merged.content = [
                    Strong(*elem.content),
                    Space,
                    *merged.content
                ]
                return []
                
            return elem

    elif isinstance(elem, Image):
        FIGURES.add_item(elem)

        # set number for caption
        fign = FIGURES.find_item(elem.identifier)
        ref = FIGURE_PREFIX(fign)
        elem.content = [ref, *elem.content]

        return elem

    elif isinstance(elem, Table):
        TABLES.add_item(elem)
        tabn = TABLES.find_item(elem.identifier)
        ref = TABLE_PREFIX(tabn)

        try:
            para = elem.caption.content[0]
        except IndexError:
            para = Para()
        caption = para.content
        caption = [ref, *caption]

        if doc.format == "latex":
            link = RawInline(
                f"\\protect\\hypertarget{{{elem.identifier}}}{{}}",
                format="tex",
            )
            elem.caption = Caption(Para(*caption, link))

        elif doc.format == "docx":
            elem.caption = Caption(Para(*caption))

        return elem


def main(doc=None):
    return run_filters([set_targets, replace_links])


if __name__ == "__main__":
    main()
