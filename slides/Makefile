.PHONY: index.html

index.html: index.md
	pandoc -t revealjs --template=template-revealjs.html --standalone --section-divs --variable transition="convex" index.md -o index.html
