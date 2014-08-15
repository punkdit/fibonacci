

out: about.pdf
	open about.pdf 


about.pdf: about.dvi
	#dvips -Ppdf about.dvi about.ps
	dvipdf about.dvi about.pdf

about.dvi: about.tex refs.bib
	latex  about
	bibtex  about
	latex  about
	latex  about

fig: compose.eps
	open compose.eps


compose.eps: render.py
	./render.py


#about.tex: _about.tex ../expr.py
#	../expr.py  _about.tex about.tex


