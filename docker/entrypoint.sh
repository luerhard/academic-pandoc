#!/bin/sh
make pdf
make docx
make diff depth=1
make clean
