#!/bin/sh

set -e
set -u

cd docs
pyreverse -o png -p rssscan --ignore=vendor ../rssscan/