#!/bin/sh

set -e
set -u

cd docs
pipenv run pyreverse -o png -p rosso --ignore=vendor ../rosso/