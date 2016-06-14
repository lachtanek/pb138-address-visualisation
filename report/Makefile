all: html pdf clean

replace_xinclude:
	hhvm replace_xinclude.hh

html: replace_xinclude
	pandoc -s -f docbook -t html5 -o report.html report.tmp.xml

pdf: replace_xinclude
	pandoc -s -f docbook --latex-engine=xelatex -o report.pdf report.tmp.xml

clean:
	rm -rf report.tmp.xml

