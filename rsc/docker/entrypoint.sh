#!/bin/sh
git config --global --add safe.directory "$PWD" # actions/runner#2033
make pdf
make diff depth=1
#make tagdiff tag="before_footnotes"
