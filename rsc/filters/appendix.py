#!/usr/bin/python3
from panflute import Div
from panflute import Plain
from panflute import RawInline
from panflute import run_filter


def action(elem, doc):

    if not doc.format == "latex":
        return None

    if isinstance(elem, Div) and elem.identifier == "beginappendix":
        elem.content = [Plain(RawInline(r"\begin{appendix}", "tex"))]
        return elem
    elif isinstance(elem, Div) and elem.identifier == "endappendix":
        elem.content = [Plain(RawInline(r"\end{appendix}", "tex"))]
        return elem


def main(doc=None):
    return run_filter(action, doc=doc)


if __name__ == "__main__":
    main()
