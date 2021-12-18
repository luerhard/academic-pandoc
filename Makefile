
all: pdf docx clean

depth ?= 1
MD_FILES ?= main.md appendix.md

COMMON_FILTERS = -F pandoc-fignos -F pandoc-secnos -F pandoc-acronyms -F pantable -F rsc/filters/appendix.py
DOCX_FILTERS = $(COMMON_FILTERS) -F rsc/filters/numbering.py
LATEX_FILTERS = $(COMMON_FILTERS) -F rsc/filters/authors_helper.py

LATEX_TEMPLATE = rsc/templates/template.tex
DOCX_TEMPLATE = rsc/templates/template.docx


md_to_tex_args := -f markdown -t latex -s --template ${LATEX_TEMPLATE} --pdf-engine pdflatex $(LATEX_FILTERS) --citeproc
pdflatex_args := -interaction batchmode -output-directory=out/ 


export PANDOC_ACRONYMS_ACRONYMS=rsc/acronyms.json

_ensure_folder:
	mkdir -p out/

_md_to_tex:
	pandoc $(md_to_tex_args) --metadata link-citations=true -o out/main.tex $(MD_FILES)
	
_md_to_docx:
	pandoc -o out/main.docx $(DOCX_FILTERS) --citeproc --reference-doc ${DOCX_TEMPLATE} $(MD_FILES)
	
_md_to_pdf:
	pandoc -o out/main.pdf $(LATEX_FILTERS) --citeproc --template $(LATEX_TEMPLATE) $(MD_FILES)

_make_diff:
	@OLD_FILES=$(nullstring)
	@for file in $(MD_FILES); do \
		OLD=$$(echo $$file | sed "s/.md/_old.md/"); \
		git show HEAD~$(depth):$$file > $$OLD; \
		OLD_FILES="$$OLD_FILES $$OLD"; \
	done
	pandoc ${md_to_tex_args} -o out/main_old.tex $$OLD_FILES
	latexdiff out/main_old.tex out/main.tex > out/diff.tex
	pdflatex $(pdflatex_args) out/diff.tex
	pdflatex $(pdflatex_args) out/diff.tex
	rm *_old.md

.ONESHELL:
diff:	_ensure_folder _make_diff

tex: _ensure_folder _md_to_tex
	
docx: _ensure_folder _md_to_docx

pdf: _ensure_folder _md_to_pdf

clean:
	rm -f out/*.log out/*.aux out/*.out out/*.tex *_old.md out/*.tdo out/*.toc
