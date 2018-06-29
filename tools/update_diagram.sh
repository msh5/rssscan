#!/bin/sh

set -e
set -u

cd docs
pyreverse -o png -p rosso --ignore=vendor ../rosso/