
all: pdf docx clean

depth ?= 1
MD_FILES ?= main.md appendix.md

DOCX_FILTERS = -F rsc/filters/numbering.py
LATEX_FILTERS = -F rsc/filters/authors_helper.py -F pandoc-fignos -F pandoc-secnos -F rsc/filters/appendix.py

LATEX_TEMPLATE = rsc/templates/template.tex
DOCX_TEMPLATE = rsc/templates/template.docx



md_to_tex_args := -f markdown -t latex -s  --template ${LATEX_TEMPLATE} --pdf-engine pdflatex $(LATEX_FILTERS) --citeproc
tex_to_docx_args := -f latex -t docx -s --reference-doc ${DOCX_TEMPLATE} ${DOCX_FILTERS}
pdflatex_args := -interaction batchmode -output-directory=out/ 


latex:
	mkdir -p out/
	pandoc $(md_to_tex_args) --metadata link-citations=true -o out/main.tex $(MD_FILES)
	
docx:
	mkdir -p out/
	pandoc $(md_to_tex_args) -o out/main.tex $(MD_FILES)
	python rsc/filters/strip_vadjust.py out/main.tex
	pandoc $(tex_to_docx_args) -o out/main.docx out/main.tex 

pdf:
	mkdir -p out/
	pandoc $(md_to_tex_args) --metadata link-citations=true -o out/main.tex $(MD_FILES)
	pdflatex $(pdflatex_args) out/main.tex
	pdflatex $(pdflatex_args) out/main.tex
	rm -f out/*.log out/*.aux out/*.out out/*.tex *_old.md out/*.tdo

.ONESHELL:
diff:	
	mkdir -p out/
	pandoc $(md_to_tex_args) --metadata link-citations=false -o out/main.tex $(MD_FILES)
	
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
	rm -f out/*.log out/*.aux out/*.out out/*.tex *_old.md

clean:
	rm -f out/*.log out/*.aux out/*.out out/*.tex *_old.md out/*.tdo
