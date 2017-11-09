#!/bin/sh
set -euf
echo "deleting virtualenv folder, if any"
rm -rf .venv
echo "creating virtualenv in .venv folder"
python3 -m venv .venv
echo "installing from requirements-dev.txt"
.venv/bin/pip3 install -r requirements-dev.txt
echo "running tests"
.venv/bin/pytest
echo "removing virtualenv folder"
rm -rf .venv

