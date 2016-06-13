all:
	hhvm replace_xinclude.hh
	pandoc -s -f docbook -o docbook.html docbook.tmp.xml
	pandoc -s -f docbook -o docbook.pdf docbook.tmp.xml
	rm -rf pandoc.tmp.xml

