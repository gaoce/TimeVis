.PHONY: clean install run uninstall

clean:
	rm -rf TimeVis.egg-info/ build/ dist/
	find . -name '*.pyc' -delete

install:
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

restart: stopdevserver
	timevis &>timevis.log &
