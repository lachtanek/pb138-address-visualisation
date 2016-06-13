all: html pdf clean

replace_xinclude:
	hhvm replace_xinclude.hh

html: replace_xinclude
	pandoc -s -f docbook --latex-engine=xelatex -o docbook.html docbook.tmp.xml

pdf: replace_xinclude
	pandoc -s -f docbook --latex-engine=xelatex -o docbook.pdf docbook.tmp.xml

clean:
	rm -rf docbook.tmp.xml

