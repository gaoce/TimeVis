.PHONY: clean install run uninstall

clean:
	rm -rf TimeVis.egg-info/ build/ dist/

install:
	python setup.py install

uninstall:
	pip uninstall -y timevis

run: install
	timevis

