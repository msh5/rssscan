#!/bin/sh

set -e
set -u

cd rosso/vendor
pipenv lock -r > requirements.txt
pipenv run pip install -t . -r requirements.txt -U
rm -rf *.egg-info *.dist-info