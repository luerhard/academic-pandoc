# Simple usage

1. Write your article in report/main.md and your appendix in reports/appendix.md
2. Push to main
3. View your results in the Actions Tab

# run with docker

```bash
# to run normally
docker run --rm -v $(pwd):/wrk lerhard/pandoc

# create custom diff (where 5 is an arbitrary number of commits)
docker run --rm -v $(pwd):/wrk --entrypoint="" lerhard/pandoc make diff depth=5
```

# local dependencies

If you want to install the software directly on your system, the following dependencies are needed:

```
- make
- TexLive 2020
- pandoc 2.16 (lower versions may work)
- python3

pypi (pip) dependencies:
- panflute
- pandoc-fignos
- pandoc-secnos
- pandoc-acronyms

```

# possible make commands
```bash
# create pdf, docx and diff with depth=1
make 

# create a pdf
make pdf

# create a word document
make docx

# create a diff pdf where depth is the number of commits to compare
make diff depth=5
```

# Implemented features

## Acronyms

To use acronyms, this repo uses [pandoc-acronyms](https://gitlab.com/mirkoboehm/pandoc-acronyms). 

The acronyms are to be specified in: `rsc/acronyms.json`and to be used in-text like this:

The most common way to write an acronym in the text is [!key]. To customize the output, the acronym specification can be made more specific:

* [!+key] selects the plural form of the acronym.
* [!^key] selects the uppercase form of the acronym. This only affects the long form, the abbreviated short form will not be changed.
* [!+^key] For plural uppercase variants, plural must be specified first.

It is also possible to select which form should be inserted into the text (this can be combined with plural or uppercase selection):

* [!key>] inserts the long form ("beer brewing attitude").
* [!key<] inserts the short form ("BBA").
* [!key!] inserts the explained form ("beer brewing attitude (BBA)").
