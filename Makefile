

supplement: supplement.tex refs2.bib
	pdflatex supplement.tex
	bibtex supplement
	pdflatex supplement.tex
	pdflatex supplement.tex



#out2: fib2
#	open fib2.pdf 

fib2: fib2.tex refs2.bib
	pdflatex fib2.tex
	bibtex fib2
	pdflatex fib2.tex
	pdflatex fib2.tex




out: fibonacci.pdf
	open fibonacci.pdf 

fibonacci.pdf: fibonacci.tex refs2.bib
	pdflatex fibonacci.tex
	bibtex fibonacci
	pdflatex fibonacci.tex
	pdflatex fibonacci.tex


