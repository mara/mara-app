# virtual env creation, package updates, db migration

# determine the right python binary
.PYTHON3:=$(shell PATH='$(subst $(CURDIR)/.venv/bin:,,$(PATH))' which python3)


setup-mara:
	make install-packages
	make -j .copy-mara-app-scripts migrate-mara-db
	echo -e "done. Get started with\n   $$ source .venv/bin/activate\n   $$ flask --help\n   $$ make run-flask"


# install exact package versions from requirements.txt.freeze
install-packages:
	make -j .venv/bin/python check-for-unpushed-package-changes
	.venv/bin/python -m pip install --upgrade pip wheel requests setuptools pipdeptree
	.venv/bin/python -m pip install --requirement=requirements.txt.freeze --src=./packages --upgrade --exists-action=w


# update packages from requirements.txt and create requirements.txt.freeze
update-packages:
	make -j check-for-unpushed-package-changes .venv/bin/python
	.venv/bin/python -m pip install --upgrade pip wheel requests setuptools pipdeptree
	PYTHONWARNINGS="ignore" .venv/bin/python -m pip install --requirement=requirements.txt --src=./packages --upgrade --exists-action=w
	make -j check-for-inconsistent-package-dependencies .copy-mara-app-scripts

# write freeze file
# pkg-ressources is automatically added on ubuntu, but breaks the install.
# https://stackoverflow.com/a/40167445/1380673
	.venv/bin/python -m pip freeze | grep -v "pkg-resources" > requirements.txt.freeze

	make check-for-newer-package-versions
	make migrate-mara-db
	echo -e "\033[32msucceeded, please check output above for warnings\033[0m"


# create or update virtualenv
.venv/bin/python:
# if .venv is already a symlink, don't overwrite it
	mkdir -p .venv

# go into the new dir and build it there as venv doesn't work if the target is a symlink
	cd .venv && $(.PYTHON3) -m venv --copies --prompt='[$(shell basename `pwd`)/.venv]' .

# set environment variables
	echo export FLASK_DEBUG=1 >> .venv/bin/activate
	echo export FLASK_APP=$(shell pwd)/app/app.py >> .venv/bin/activate

# on Mac, some operations in a multiprocessing environment crash Python with this message:
#     +[__NSCFConstantString initialize] may have been in progress in another thread when fork() was called.
#     We cannot safely call it or ignore it in the fork() child process. Crashing instead.
#     Set a breakpoint on objc_initializeAfterForkError to debug.
#
# See https://stackoverflow.com/questions/50168647/multiprocessing-causes-python-to-crash-and-gives-an-error-may-have-been-in-progr
	echo export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES >> .venv/bin/activate

# On Mac, some http operations in a multiprocessing environment segfault Python with this message:
#     EXC_BAD_ACCESS (SIGSEGV)
#      .. crashed on child side of fork pre-exec
#
# See https://blog.yimingliu.com/2015/07/22/python-multiprocessing-code-crashes-on-os-x-under-ipython/
	echo export no_proxy='*' >> .venv/bin/activate

# add the project directory to path
	echo $(shell pwd) > `echo .venv/lib/*/site-packages`/mara-path.pth

# install minimum set of required packages
# wheel needs to be early to be able to build wheels
	.venv/bin/python -m pip install --upgrade pip wheel requests setuptools pipdeptree

# Workaround problems with un-vendored urllib3/requests in pip on ubuntu/debian
# This forces .venv/bin/pip to use the vendored versions of urllib3 from the installed requests version
# see https://stackoverflow.com/a/46970344/1380673
	-rm -vf .venv/share/python-wheels/{requests,chardet,urllib3}-*.whl


# auto-migrate the mara db
migrate-mara-db:
	FLASK_APP=app/app.py .venv/bin/flask mara_db.migrate


# run flask development server
run-flask:
	. .venv/bin/activate; flask run --with-threads --reload --eager-loading 2>&1


# run https://github.com/naiquevin/pipdeptree to check whether the currently installed packages have
# incompatible dependencies
check-for-inconsistent-package-dependencies:
	.venv/bin/pipdeptree --warn=fail


# check whether there are unpushed changes in the /packages directory
check-for-unpushed-package-changes:
	make -j .check-for-unpushed-package-changes

.check-for-unpushed-package-changes: $(addprefix .ensure-pushed-,$(subst ./,,$(shell mkdir -p packages; cd packages; find . -maxdepth 1 -mindepth 1 -type d)))

.ensure-pushed-%:
	.scripts/mara-app/ensure-pushed.sh packages/$*


# check whether there are newer versions of the installed packages available
check-for-newer-package-versions:
	make -j .check-for-newer-package-versions

.check-for-newer-package-versions: $(addprefix .check-newer-,$(subst ./,,$(shell cd packages; find . -maxdepth 1 -mindepth 1 -type d)))

.check-newer-%:
	.scripts/mara-app/check-newer.sh packages/$*


# remove virtual env
.cleanup-vitualenv: .check-for-unpushed-package-changes
	rm -rf .venv
	rm -rf packages