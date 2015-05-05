.PHONY: clean install run uninstal devserver stopdevserver restart

clean:
	rm -rf TimeVis.egg-info/ build/ dist/
	find . -name '*.pyc' -delete

install:
	@ if [ -e timevis/db/*.db ]; then rm timevis/db/*.db; fi
	@ touch timevis/db/timevis.db
	python setup.py install

uninstall:
	pip uninstall -y timevis

run: install
	timevis &>timevis.log &

devserver:
	python timevis/app.py

stopdevserver:
	pkill timevis
	pkill python

restart: stopdevserver run
