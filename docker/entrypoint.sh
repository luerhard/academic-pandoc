#!/bin/sh
make pdf
make docx
make diff depth=2
make clean
