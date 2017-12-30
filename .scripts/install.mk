# virtual env creation, package updates, db migration

# determine the right python binary
.PYTHON36:=$(shell PATH=$(subst $(CURDIR)/.venv/bin:,,$(PATH)) which python3.6)


setup-mara:
	make install-packages
	make -j .copy-mara-app-scripts migrate-mara-db
	echo -e "done. Get started with\n   $$ source .venv/bin/activate\n   $$ flask"


# install exact package versions from requirements.txt.freeze
install-packages:
	make -j .venv/bin/python check-for-unpushed-package-changes
	.venv/bin/pip install --requirement=requirements.txt.freeze --src=./packages --upgrade


# update packages from requirements.txt and create requirements.txt.freeze
update-packages:
	make -j check-for-unpushed-package-changes .venv/bin/python
	PYTHONWARNINGS="ignore" .venv/bin/pip install --requirement=requirements.txt --src=./packages --upgrade --process-dependency-links
	make -j check-for-inconstent-package-dependencies .copy-mara-app-scripts
	# write freeze file
	# pkg-ressources is automatically added on ubuntu, but breaks the install.
	# https://stackoverflow.com/a/40167445/1380673
	.venv/bin/pip freeze | grep -v "pkg-resources" > requirements.txt.freeze
	make migrate-mara-db
	echo -e "\033[32msucceeded, please check output above for warnings\033[0m"


# create or update virtualenv
.venv/bin/python: 
	# if .venv is already a symlink, don't overwrite it
	mkdir -p .venv
	# go into the new dir and build it there as venv doesn't work if the target is a symlink
	cd .venv && $(.PYTHON36) -m venv --copies --prompt='[$(shell basename `pwd`)/.venv]' .
	# set environment variables
	echo export FLASK_DEBUG=1 >> .venv/bin/activate
	echo export FLASK_APP=$(shell pwd)/app/app.py >> .venv/bin/activate
	# add the project directory to path
	echo $(shell pwd) > `echo .venv/lib/*/site-packages`/mara-path.pth
	# install minimum set of required packages
	.venv/bin/pip install --upgrade pip setuptools pipdeptree wheel


# auto-migrate the mara db
migrate-mara-db:
	FLASK_APP=app/app.py .venv/bin/flask mara_app.migrate


# run https://github.com/naiquevin/pipdeptree to check whether the currently installed packages have
# incompatible dependencies
check-for-inconstent-package-dependencies:
	.venv/bin/pipdeptree --warn=fail


# check whether there are unpushed changes in the /packages directory
check-for-unpushed-package-changes: $(addprefix .ensure-pushed-,$(subst ./,,$(shell mkdir -p packages; cd packages; find . -maxdepth 1 -mindepth 1 -type d)))

.ensure-pushed-%:
	.scripts/mara-app/ensure-pushed.sh packages/$*


