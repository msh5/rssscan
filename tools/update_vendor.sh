#!/bin/sh

set -e
set -u

cd rssscan/vendor
pipenv lock -r > requirements.txt
pip install -t . -r requirements.txt -U
rm -rf *.egg-info *.dist-info
