#!/bin/sh
#ensure that a command error aborts the whole script
set -euf
echo "deleting virtualenv folder, if any"
rm -rf .venv
echo "creating virtualenv in .venv folder"
python3 -m venv .venv
echo "installing from requirements-dev.txt"
.venv/bin/pip install -e . --process-dependency-links --allow-all-external
echo "running tests"
.venv/bin/pytest
echo "👍 installation and test OK 👍"
echo "removing virtualenv folder"
rm -rf .venv

