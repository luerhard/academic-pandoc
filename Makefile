
all: pdf docx clean

depth ?= 1
MD_FILES ?= main.md appendix.md

COMMON_FILTERS = -F pantable -F pandoc-acronyms -F rsc/filters/crossref.py -F rsc/filters/appendix.py --highlight-style=tango
DOCX_FILTERS = $(COMMON_FILTERS)
LATEX_FILTERS = $(COMMON_FILTERS) -F rsc/filters/authors_helper.py

LATEX_TEMPLATE = rsc/templates/template.tex
DOCX_TEMPLATE = rsc/templates/template.docx


md_to_tex_args := -f markdown -t latex -s --template ${LATEX_TEMPLATE} --pdf-engine pdflatex $(LATEX_FILTERS) --citeproc
pdflatex_args := -interaction nonstopmode -output-directory=out/ 

export PANDOC_ACRONYMS_ACRONYMS=rsc/acronyms.json

_ensure_folder:
	mkdir -p out/

_md_to_tex:
	pandoc $(md_to_tex_args) --metadata link-citations=true -o out/main.tex $(MD_FILES)
	
_tex_to_docx:
	pandoc -o out/main.docx $(DOCX_FILTERS) --citeproc --reference-doc $(DOCX_TEMPLATE) out/main.tex
	
_tex_to_docx_filter:
	python rsc/filters/strip_vadjust.py out/main.tex
	
_md_to_docx:
	pandoc -o out/main.docx $(DOCX_FILTERS) --citeproc --reference-doc $(DOCX_TEMPLATE) $(MD_FILES)
	
_md_to_pdf:
	pandoc -o out/main.pdf $(LATEX_FILTERS) --citeproc --metadata link-citations=true --template $(LATEX_TEMPLATE) $(MD_FILES)

.ONESHELL:
_make_diff:
	OLD_FILES=$(nullstring)
	for file in $(MD_FILES); do \
		OLD=$$(echo $$file | sed "s/.md/_old.md/"); \
		git show HEAD~$(depth):$$file > out/$$OLD; \
		OLD_FILES="$$OLD_FILES out/$$OLD"; \
	done
	pandoc -o out/main_old.tex ${md_to_tex_args} $$OLD_FILES
	pandoc -o out/main_new.tex ${md_to_tex_args} $(MD_FILES)
	latexdiff out/main_old.tex out/main_new.tex --replace-context2cmd="\author" --config="PICTUREENV=(?:picture|DIFnomarkup|align|tabular|longtable)[\w\d*@]*" -t CCHANGEBAR --append-safecmd="(enquote|enquote\*)" > out/diff_$(depth)_commits.tex
	pdflatex $(pdflatex_args) out/diff_$(depth)_commits.tex
	pdflatex $(pdflatex_args) out/diff_$(depth)_commits.tex

.ONESHELL:
_make_timediff:
	OLD_FILES=$(nullstring)
	for file in $(MD_FILES); do \
		OLD=$$(echo $$file | sed "s/.md/_old.md/"); \
		git show `git rev-list -n 1 --before="$(at)" main`:$$file > out/$$OLD; \
		OLD_FILES="$$OLD_FILES out/$$OLD"; \
	done
	pandoc -o out/main_old.tex ${md_to_tex_args} $$OLD_FILES
	pandoc -o out/main_new.tex ${md_to_tex_args} $(MD_FILES)
	DIFFNAME=out/diff_$$(echo $$at | sed s"/[[:space:]]/_/g" | sed s"/\:/-/g").tex
	latexdiff out/main_old.tex out/main_new.tex --replace-context2cmd="\author|\caption" --config="PICTUREENV=(?:picture|DIFnomarkup|align|tabular|longtable)[\w\d*@]*" -t CCHANGEBAR --append-safecmd="(enquote|enquote\*)" > $$DIFFNAME
	pdflatex $(pdflatex_args) $$DIFFNAME
	pdflatex $(pdflatex_args) $$DIFFNAME

.ONESHELL:
_make_tagdiff:
	OLD_FILES=$(nullstring)
	for file in $(MD_FILES); do \
		OLD=$$(echo $$file | sed "s/.md/_old.md/"); \
		git show $(tag):$$file > out/$$OLD; \
		OLD_FILES="$$OLD_FILES out/$$OLD"; \
	done
	pandoc -o out/main_old.tex ${md_to_tex_args} $$OLD_FILES
	pandoc -o out/main_new.tex ${md_to_tex_args} $(MD_FILES)
	DIFFNAME=out/diff_$$(echo $(tag) | sed s"/[[:space:]]/_/g" | sed s"/\:/-/g").tex
	latexdiff out/main_old.tex out/main_new.tex --replace-context2cmd="\author"  --config="PICTUREENV=(?:picture|DIFnomarkup|align|tabular|longtable)[\w\d*@]*" -t CCHANGEBAR --append-safecmd="(enquote|enquote\*)" > $$DIFFNAME
	pdflatex $(pdflatex_args) $$DIFFNAME
	pdflatex $(pdflatex_args) $$DIFFNAME

clean:
	rm -f out/*.log out/*.aux out/*.out out/*.tdo out/*.toc out/*_old.tex out/*_new.tex out/*_old.md out/diff_*.tex out/*.cb out/*.cb2

timediff: _ensure_folder _make_timediff clean

diff: _ensure_folder _make_diff clean

tagdiff: _ensure_folder _make_tagdiff clean

tex: _ensure_folder _md_to_tex

docx: _ensure_folder _md_to_docx

latex_docx: _ensure_folder _md_to_tex _tex_to_docx_filter _tex_to_docx

pdf: _ensure_folder _md_to_pdf


