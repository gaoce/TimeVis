.PHONY: init-db clean install uninstall run devserver stop-devserver restart-devserver local stop-local restart-local

init-db:
	cp test/timevis.db timevis/db/

clean:
	rm -rf TimeVis.egg-info/ build/ dist/ *.log
	find . -name '*.pyc' -delete

install: clean
	@ if [ -e timevis/db/*.db ]; then rm timevis/db/*.db; fi
	@ touch timevis/db/timevis.db
	python setup.py install

uninstall:
	pip uninstall -y timevis

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

local-bg: init-db
	python run.py &

stop-local:
	pkill python

restart-local: stop-local local

local-test:
	cd test; make -f Makefile all

github:
	@echo "Issue this command after checking out to gh-pages branch"
	git checkout master -- docs
	cp -r docs/_build/html/* .
	git add .
	git commit -m "Update github pages"
	git push origin gh-pages
