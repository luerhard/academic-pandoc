#!/bin/sh
make pdf
make docx
make diff depth=10
make clean
