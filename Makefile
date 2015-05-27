.PHONY: github

github:
	cd docs; make html
	cp -r docs/_build/html/* .
	git add .
	git commit -m "Update github pages"
	git push origin gh-pages
