# Simple usage

1. Write your article in report/main.md and your appendix in reports/appendix.md
2. Push to main
3. View your results in the Actions Tab

# run with docker

```bash
# to run normally
docker run --rm -v $(pwd):/wrk lerhard/pandoc

# create custom diff (where 5 is an arbitrary number of commits)
docker run --rm -v $(pwd):/wrk --entrypoint="" lerhard/pandoc make diff depth=5
```

# local dependencies

If you want to install the software directly on your system, the following dependencies are needed:

```
- make
- TexLive 2020
- pandoc 2.16 (lower versions may work)
- python3

pypi (pip) dependencies:
- panflute
- pandoc-fignos
- pandoc-secnos
```

# possible make commands
```bash
# create pdf, docx and diff with depth=1
make 

# create a pdf
make pdf

# create a word document
make docx

# create a diff pdf where depth is the number of commits to compare
make diff depth=5
```
