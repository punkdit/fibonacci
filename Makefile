

out: fibonacci.pdf
	open fibonacci.pdf 

fibonacci.pdf: fibonacci.tex refs2.bib
	pdflatex fibonacci.tex
	bibtex fibonacci
	pdflatex fibonacci.tex
	pdflatex fibonacci.tex


