MODULE_NAME=mara_app
JQUERY_VERSION ?= 3.5.1
JQUERY_FLOATTHEAD_VERSION ?= 2.2.4
BOOTSTRAP_VERSION ?= 4.6.1

all:
	# builds virtual env. and starts install in it
	make .venv/bin/python
	make install


install:
	# install of module
	.venv/bin/pip install .


test:
	make .venv/bin/python
	# test of module
	.venv/bin/pip install .[test]
	.venv/bin/pytest


publish:
	# manually publishing the package
	.venv/bin/pip install build twine
	.venv/bin/python -m build
	.venv/bin/twine upload dist/*


clean:
	# clean up
	rm -rf .venv/ build/ dist/ ${MODULE_NAME}.egg-info/ .pytest_cache/ .eggs/


.PYTHON3:=$(shell PATH='$(subst $(CURDIR)/.venv/bin:,,$(PATH))' which python3)

.venv/bin/python:
	mkdir -p .venv
	cd .venv && $(.PYTHON3) -m venv --copies --prompt='[$(shell basename `pwd`)/.venv]' .

	.venv/bin/python -m pip install --upgrade pip

download-jquery:
	curl https://cdn.jsdelivr.net/npm/jquery@$(JQUERY_VERSION)/dist/jquery.min.js -o mara_app/static/jquery.min.js

download-jquery-floatThead:
	curl https://cdnjs.cloudflare.com/ajax/libs/floatthead/$(JQUERY_FLOATTHEAD_VERSION)/jquery.floatThead.min.js -o mara_app/static/jquery.floatThead.min.js

download-bootstrap:
	curl https://cdn.jsdelivr.net/npm/bootstrap@$(BOOTSTRAP_VERSION)/dist/css/bootstrap.min.css -o mara_app/static/bootstrap/bootstrap.min.css
	curl https://cdn.jsdelivr.net/npm/bootstrap@$(BOOTSTRAP_VERSION)/dist/css/bootstrap.min.css.map -o mara_app/static/bootstrap/bootstrap.min.css.map
	curl https://cdn.jsdelivr.net/npm/bootstrap@$(BOOTSTRAP_VERSION)/dist/js/bootstrap.min.js -o mara_app/static/bootstrap/bootstrap.min.js
