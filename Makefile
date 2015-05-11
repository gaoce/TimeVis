.PHONY: init-db clean install uninstall run devserver stop-devserver restart-devserver local stop-local restart-local

# Remove database file and initiate a new one
init-db:
	rm timevis/db/timevis.db
	touch timevis/db/timevis.db

# Clean unnecessary files that come with installation process
clean:
	rm -rf TimeVis.egg-info/ build/ dist/ *.log
	find . -name '*.pyc' -delete

# Install a new version of package to local system
install: clean
	@ if [ -e timevis/db/*.db ]; then rm timevis/db/*.db; fi
	@ touch timevis/db/timevis.db
	python setup.py install

# Uninstall
uninstall:
	pip uninstall -y timevis

# Run the software in local system
run: install
	timevis &>timevis.log &

devserver:
	python timevis/app.py

stop-devserver:
	pkill timevis
	pkill python

restart-devserver: stopdevserver run

# Run without deployment
local: init-db
	python run.py

stop-local:
	pkill python

restart-local: stop-local local

github:
	@echo "!!NOTE: Issue this command after checking out to gh-pages branch"
	git checkout master -- docs
	cp -r docs/_build/html/* .
	git add .
	git commit -m "Update github pages"
	git push origin gh-pages
