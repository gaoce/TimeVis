.PHONY: clean install uninstall init-db devserver stop-devserver restart-devserver test github

clean:
	rm -rf TimeVis.egg-info/ build/ dist/ *.log
	find . -name '*.pyc' -delete

# Install the application (locally)
install:
	@if [ -e timevis/db/*.db ]; then rm timevis/db/*.db; fi
	python setup.py install -q

# Uninstall the application
uninstall:
	pip uninstall -y timevis

# Copy existing database file
init-db:
	cp test/timevis.db timevis/db/

# Run developmental server
devserver:
	python dev.py

# Stop developmental server
stop-devserver:
	pkill python

# Restart
restart-devserver: stop-devserver devserver

# Test API
test:
	@python -m unittest discover

# Update docs
update-doc:
	git checkout gh-pages -- docs

docker:
	sudo docker build . -t gaoce/timevis:lastest
