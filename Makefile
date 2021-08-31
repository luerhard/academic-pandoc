
all: pdf docx clean

depth := 1
markdown-files := report/main.md report/appendix.md

FILTERS = -F resources/filters/authors_helper.py -F pandoc-fignos -F pandoc-secnos -F resources/filters/appendix.py

args_pandoc_tex := -f markdown -t latex --standalone --template resources/templates/template.tex --pdf-engine pdflatex --resource-path resources/ ${FILTERS} --citeproc

args_docx_tex := -f latex -t docx --standalone --reference-doc resources/templates/template.docx -F resources/filters/numbering.py


latex:
	@pandoc $(args_pandoc_tex) \
		--metadata link-citations=true \
		-o out/main.tex \
		 $(markdown-files)
		
		
docx:
	@pandoc $(args_pandoc_tex) \
		-o out/main.tex \
		 $(markdown-files)
		
	@python resources/filters/strip_vadjust.py out/main.tex
		
	@pandoc $(args_docx_tex) \
		-o out/main.docx \
		out/main.tex 

_docx:
	@pandoc $(args_docx_tex) \
		-o out/main.docx \
		out/main.tex 

_docx_raw:
	@pandoc -f markdown -t docx --standalone --reference-doc resources/templates/template.docx  -F pandoc-fignos -F pandoc-secnos -F resources/filters/numbering.py --citeproc -o out/test.docx ${markdown-files}
		
_pdf:
	pdflatex -output-directory=out/ out/main.tex
	pdflatex -output-directory=out/ out/main.tex
	

pdf:
	@pandoc $(args_pandoc_tex) \
		--metadata link-citations=true \
		-o out/main.tex \
		 $(markdown-files)

	@pdflatex -output-directory=out/ out/main.tex
	@pdflatex -output-directory=out/ out/main.tex


diff:
	@pandoc $(args_pandoc_tex) \
		--metadata link-citations=false \
		-o out/main.tex \
		 $(markdown-files)
	@git show HEAD~$(depth):report/main.md > report/main_old.md
	@git show HEAD~$(depth):report/appendix.md > report/appendix_old.md
	@pandoc -d defaults/tex.yaml -o out/main_old.tex report/main_old.md report/appendix_old.md 
	@latexdiff out/main_old.tex out/main.tex > out/diff.tex
	@pdflatex -output-directory=out/ out/diff.tex
	@pdflatex -output-directory=out/ out/diff.tex
	@rm report/main_old.md report/appendix_old.md out/main_old.tex

clean:
	rm -f out/*.log out/*.aux out/*.out out/*.tex
