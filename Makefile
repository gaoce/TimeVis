.PHONY: clean install run uninstall

clean:
	rm -rf TimeVis.egg-info/ build/ dist/
	find . -name '*.pyc' -delete

install:
	python setup.py install

uninstall:
	pip uninstall -y timevis

run: install
	timevis

devserver:
	python timevis/app.py

