.PHONY: clean install uninstall init-db devserver stop-devserver restart-devserver test github

clean:
	rm -rf TimeVis.egg-info/ build/ dist/ *.log
	find . -name '*.pyc' -delete

# Install the application (locally)
install: clean
	@if [ -e timevis/db/*.db ]; then rm timevis/db/*.db; fi
	python setup.py install -q

# Uninstall the application
uninstall:
	pip uninstall -y timevis

# Copy existing database file
init-db:
	cp test/timevis.db timevis/db/

# Run developmental server
devserver: init-db
	python run.py

# Stop developmental server
stop-devserver:
	pkill python

# Restart
restart-devserver: stop-devserver devserver

# Test API
test:
	cd test; make -f Makefile all

# Publish documentation to github page
github:
	@echo "Issue this command after checking out to gh-pages branch"
	git checkout master -- docs
	cp -r docs/_build/html/* .
	git add .
	git commit -m "Update github pages"
	git push origin gh-pages
