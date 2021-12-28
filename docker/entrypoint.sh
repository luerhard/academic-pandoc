#!/bin/sh
make pdf
make docx
make diff depth=1
make diff depth=20
make timediff at="yesterday"
make timediff at="2021-12-22 09:00"
