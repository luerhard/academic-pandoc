# Simple usage

1. Write your article in report/main.md and your appendix in reports/appendix.md
2. Push to main
3. View your results in the Actions Tab

# run with docker

```bash
# to create a pdf on Linux or Mac
docker run --rm -v $(pwd):/wrk lerhard/pandoc:3.1.2-1 make pdf

# to create a pdf on PowerShell (Windows) it might be necessary to write:
docker run --rm -v ${PWD}:/wrk lerhard/pandoc:3.1.2-1 make pdf

# for Windows Command Line, use
docker run --rm -v %cd%:/wrk lerhard/pandoc:3.1.2-1 make pdf

# create custom diff (where 5 is an arbitrary number of commits)
docker run --rm -v $(pwd):/wrk lerhard/pandoc:3.1.2-1 make diff depth=5
```

# Features and documentation

Please see the actions tab or compile this template to get a full documentation.
If anything is left unclear, pleas do not hesitate to open an issue.
