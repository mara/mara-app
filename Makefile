JQUERY_VERSION ?= 3.5.1
JQUERY_FLOATTHEAD_VERSION ?= 2.2.4
BOOTSTRAP_VERSION ?= 4.6.1

all:
	@echo "You can use target 'upgrade-bootstrap' to upgrade bootstrap and jquery"

download-jquery:
	curl https://cdn.jsdelivr.net/npm/jquery@$(JQUERY_VERSION)/dist/jquery.min.js -o mara_app/static/jquery.min.js

download-jquery-floatThead:
	curl https://cdnjs.cloudflare.com/ajax/libs/floatthead/$(JQUERY_FLOATTHEAD_VERSION)/jquery.floatThead.min.js -o mara_app/static/jquery.floatThead.min.js

download-bootstrap:
	curl https://cdn.jsdelivr.net/npm/bootstrap@$(BOOTSTRAP_VERSION)/dist/css/bootstrap.min.css -o mara_app/static/bootstrap/bootstrap.min.css
	curl https://cdn.jsdelivr.net/npm/bootstrap@$(BOOTSTRAP_VERSION)/dist/css/bootstrap.min.css.map -o mara_app/static/bootstrap/bootstrap.min.css.map
	curl https://cdn.jsdelivr.net/npm/bootstrap@$(BOOTSTRAP_VERSION)/dist/js/bootstrap.min.js -o mara_app/static/bootstrap/bootstrap.min.js

download-web-packages:
	make -j upgrade-jquery upgrade-bootstrap