#!/bin/sh
make pdf
make docx
make diff depth=1
make timediff at="2021-12-24 00:55"
