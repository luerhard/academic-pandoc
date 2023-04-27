from panflute import run_filter
from panflute import Citation
from panflute import Str

# for debugging uncomment and use logger.
# import logging
# logging.basicConfig(filename="crossref.txt", filemode="w")
# logger = logging.getLogger()

REPLACEMENT = "and"


def replace_intext_cite(elem, doc):
    global REPLACEMENT

    if isinstance(elem, Citation) and elem.mode == "AuthorInText":
        citation = elem.ancestor(1)

        replaced_citation = []
        for token in citation.content:
            if token == Str("&"):
                replaced_citation.append(Str(REPLACEMENT))
            else:
                replaced_citation.append(token)

        citation.content = replaced_citation


def main(doc=None):
    return run_filter(replace_intext_cite)


if __name__ == "__main__":
    main()
