---
# Bibliography
csl: rsc/library/style.csl # See https://www.zotero.org/styles for more styles.
bibliography: rsc/library/references.json

title: 'Academic-Pandoc Template'

authors:
    - John Doe:
        institute: [inst1, inst2]
        email: john@doe.com
    - Jane Doe:
        institute: inst1
    - Jack Barnes:
        institute: inst3
        email: jack.barnes@cl.cam.ac.uk.com
        correspondence: yes

institutes:
    inst1: Institute for social sciences, University of Stuttgart, Stuttgart, BW, Germany
    inst2: Dep. Social Science, University of Wuppertal, Wuppertal, NRW, Germany
    inst3: Computer Laboratory, Cambridge University, JJ Thomson Avenue, Cambridge

date: \today

abstract: 'This is a template this is designed to make it as easy as possible to create scientific publications in social science journals. To use this, just create a new repo from this template, clear the example text from main.md and appendix.md, and start writing. The current content of this document explains all functionalities.'

keywords: 'Key, Words'

titlepage: true
toc: true # Table of contents

---

# Introduction {#sec:introduction}

This is supposed to be a battery-included template to create publication ready documents from markdown.
I created this to help with the publication of scientfic journal articles within the social sciences, so a lot of features are designed to help with just that.

# Features {#sec:features}

This section shows a list of implemented features to help with the simple creation of manuscripts.
All features are listed in alphabetical order to make it easy to find the im the table of contents.

## Acronyms {#sec:acronyms}

Acronyms are implemented using the [pandoc-acronyms](https://gitlab.com/mirkoboehm/pandoc-acronyms) filter.
To create an acronym, go the the file `rsc/acronyms.json` and fill in all the acronyms you need.
The following snippet shows how to structure this document:

```json
{
 "aba": {
 "shortform": "ABA",
 "longform": "a better acronym"
 },
 "bba": {
 "shortform": "BBA",
 "longform": "beer brewing attitude"
 }
}
``` 
The most common way to write an acronym in the text is `[!key]`. 
Writing `[!aba]`, for example, results in: [!aba] at the first in-text mention and as [!aba] in all subsequent mentions.
To customize the output, the acronym specification can be made more specific:

* `[!+key]` selects the plural form of the acronym.
* `[!^key]` selects the uppercase form of the acronym. This only affects the long form, the abbreviated short form will not be changed.
* `[!+^key]` For plural uppercase variants, plural must be specified first.

It is also possible to select which form should be inserted into the text (this can be combined with plural or uppercase selection):

* `[!key>]` inserts the long form ("beer brewing attitude").
* `[!key<]` inserts the short form ("BBA").
* `[!key!]` inserts the explained form ("beer brewing attitude (BBA)").

## Appendix {#sec:the-appendix}
The appendix is best written into the existing file `appendix.md`.
Everything that is written inside the Div-block `.appendix` is considered to be the Appendix:
```markdown
::::: {.appendix}
# Appendices {.unnumbered}

Everything between the ::::: is considered to be Appendix.
The Header is optional.
:::::
```

Sections in the Appendix are numbered by letters, starting with @ap:super_important.
Subsections are named Appendix @ap:subappendix, then Appendix @ap:subsub, and so forth.
The maximum depth for all Section numbering here currently is 3, so do not use Appendices more nested than that.
To change that, it would be necessary to define deeper levels in `rsc/filters/crossref.py` in the variable: `LATEX_SECTION_MAPPER`.
This, however, is untested – most journal will not allow more than two levels of section-nesting anyway.

Tables (cf. Section @sec:tables) and Figures (cf. Section @sec:figures) in  Appendix @ap:super_important are numbered separately as as A1, A2 etc., and start again with B1, B2 etc. for Appendix @ap:B, following the style guide of the [!apa]. 

## Citations {#sec:citations}

Citations are stored in `rsc/library/references.json`.

They can be used as in-text with: @boswell:MigrationEuropepaper.2005 or in parentheses with [@boswell:MigrationEuropepaper.2005].

The style for the references is a CSL Stylesheet in `rsc/library/style.csl`. It defaults to APA7.

Both paths can be changed in the header of `main.md`.


## Figures {#sec:figures}

This is how to add images:

![This is not a cat !](rsc/images/Figure_1.eps){#fig:timeline .center width="100%"}

This can be referenced using the tag Figure @fig:timeline.
Currently, .eps, .jpg, and .png files are supported.
Figures in the Appendix are numbered differently as you can see with @fig:catpic_A from Appendix @ap:super_important or Figure @fig:catpic_B from Appendix @ap:subsub.

## Footnotes {#sec:footnotes}

[^key]: Content of footnote.

Footnotes are created by defining `[^key]: Content of footnote.` anywhere in the document[^key] and can be referenced using `[^key]`. 
The key can be any character string without spaces.
I would recommend defining footnotes at the end of the paragraph[^goodplace]
Currently not possible in pandoc is referencing the same footnote multiple times[^key]. This results in a duplication of the footnote.

[^goodplace]: This is a good place for a footnote.

Endnotes are also not implemented due to limitations of pandoc.
The easiest way to achieve endnotes in docx is to manually redefine footnotes to endnotes after compilation.
There should exist an easier way for latex (and therefore pdf), but it is not implemented (yet). 

## Markdown Syntax {#sec:markdown-syntax}

You can write any valid **Markdown**. 
If this is not enough, \textit{Latex} commands are also _available_. 
Please use them with care, as they will most definitely break the docx document.

## Table of Contents

The table of contents can be activated by setting `toc: true` in the header of `main.md`.
To deactivate it, set `toc: false`.

## Tables {#sec:tables}

This is how to include tables from csv files via `pantable` :

```{.table #tbl:test}
---
alignment: LLL
caption: Example Table from csv
width: [0.2,0.2,0.2]
include: rsc/tables/sample.csv
markdown: true
---
```

You can also create tables within the document.

``` {.table #tbl:possible_commands}
---
alignment: LLL
caption: Possible commands for pantable
header: true
markdown: true
table-width: 1.0
width: [0.2,0.2,0.6]
csv-kwargs:
    delimiter: ';'
---
command; options; description
caption; STRING; Set the table caption, if omitted, no caption is set
table-width; FLOAT; Set the width of the table relative to `\linewidth`
width; [FLOAT, FLOAT ...]; Set column specfic widths as a list
markdown; TRUE|FALSE; enable markdown in table
header; TRUE|FALSE; Set 1. row as a header
```

You can reference Table @tbl:possible_commands like this.
Table @tbl:desc are named differently.

## Titlepage {#sec:titlepage}

The table of contents can be activated by setting `titlepage: true` in the header of `main.md`.
To deactivate it, set `titlepage: false`.

## ToDo Notes {#sec:todos}

Classical Latex ToDo-Notes are also possible.
Note, however, that those will not show up in the docx Version of the Document.

Lorem Ipsum comes from sections 1.10.32 and 1.10.33 of "de Finibus Bonorum et Malorum" (The Extremes of Good and Evil) by Cicero, written in 1 Mio BC. This book is a treatise on the theory of ethics, very popular during the Renaissance.
The first line of Lorem Ipsum, "Lorem ipsum dolor sit amet..", comes from a line in section 1.10.32.
\todo[author=MM]{This needs to be changed}
\todo[author=KU]{I'm on it}

## Sections {#sec:sections}

Sections are numbered and included into the toc up to a depth of 3.

#### Markdown headers of depth 4 

are unnumbered paragraph headers (followed by a newline) as seen above 

##### headers of depth 5 

are inlined paragraph titles (bold at the start of the paragraph).


## Section References {#sec:links-to-sections}

Similiar to links to figures (see Section @sec:figures), sections can be referenced.
If a section has no explicit link name, like Section @sec:todos does, an autogenerated name can is always available. It is usually lowercased and spaced are replaced by a dash: `-`.


# Output

The output is set via `make` commands and have a couple of different options.
Multiple outputs can be specified in `rsc/docker/entrypoint.sh`.
They will all be run, once new commits are pushed to the main branch of your repository.

An example entrypoint file could look like:

```bash
# creates a pdf from the latest commit
make pdf

# creates a docx version of the latest commit
make docx

# creates a diff wrt to the commit with the tag "first_submission"
make tagdiff tag="first_submission"
```

If you want to create your files locally, the best way is to use docker, see [https://docs.docker.com/engine/install/](https://docs.docker.com/engine/install/) on how to install it.
Once installed, all commands can be run follwing this scheme:

```bash
# to create a pdf on Linux or Mac
docker run --rm -v $(pwd):/wrk lerhard/pandoc:2.18-2 make pdf

# to create a pdf on PowerShell, it might be necessary to write:
docker run --rm -v ${PWD}:/wrk lerhard/pandoc:2.18-2 make pdf

# for Windows Command Line, use
docker run --rm -v %cd%:/wrk lerhard/pandoc:2.18-2 make pdf
```

If you want to use a newer container, check [https://hub.docker.com/r/lerhard/pandoc](https://hub.docker.com/r/lerhard/pandoc) for new container releases and update the tag (`2.18-2` in this case).

## pdf

The `make pdf` command is possibly the most used one.
It just creates a pdf from based on `HEAD`.
To modify the style of the resulting document, changes can be made to the Latex template `rsc/templates/template.tex`.
If you want to use a different template instead, modify the `LATEX_TEMPLATE` variable in `Makefile`.

## docx
The `make docx` command creates a docx version of the manuscript based `HEAD`.
To modify the style of the resulting document, changes can be to the docx template `rsc/templates/template.docx`.
If you want to use a different template instead, modify the `DOCX_TEMPLATE` variable in `Makefile`.

## Diffs

To facilitate working with multiple authors on the same document, it can be very useful to create diffs, thus highlighting specific changes made to the document.
In academic-pandoc, there are currenty three different commands to create diffs targeted to specific usecases.

### diff

The most basic command is `make diff`.
The `make diff depth=n` command creates a diff where `n` specifices the number of commits.
Setting `make diff depth=1` (the default value is 1) therefore creates a diff to the last commit, showing all changes made in the most recent commit.
This command produces files with the naming pattern `diff_n.pdf`.

### tagdiff

The command `make tagdiff tag="tagname"` creates a diff based on a specific tag or commit hash.
Setting `make tagdiff tag="43147e3"`, for example, would create a diff with respect to commit 43147e3.
This can be especially useful when you are working on a revision of your manuscript, thus allowing academic-pandoc to create a fixed diff to the last submission.
This command produces files with the naming pattern `diff_tagname.pdf`.
It is therefore recommended to use tags instead of hashes for better filename readability.
If you want to use tags, you can create a git tag `first_submission`, using

```bash
# creates a tag for the latest commit
git tag -a first_submission

# creates a tag for the commit 43147e3
git tag -a first_submission 43147e3

# removes tag first_submission
git tag -d first_submission
```

Do not forget to push your tags, using `git push --tags`.

### timediff

If you do not want to use commit hashes or tags, or you just have been off for a week and want to see the latest changes on the manuscript, you can use `make timediff at="2021-12-31 12:00"`.
This will create a diff to commit that is closest to (but before) the timestamp you specified.
This command produces files with the naming pattern `diff_timestamp.pdf`.

## latex

The `make latex` command creates the raw tex version of your manuscript based on `HEAD`.
This can be useful if Latex is the required submission format.






