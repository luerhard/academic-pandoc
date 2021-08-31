# Simple usage

1. Write your article in report/main.md and your appendix in reports/appendix.md
2. Push to main
3. View your results in the Actions Tab

# run locally

```bash
# to run normally
docker run --rm --workdir /wrk -v $(pwd):/wrk lerhard/pandoc

# create custom diff (where 5 is an arbitrary number of commits)
docker run --rm --workdir /wrk -v $(pwd):/wrk --entrypoint="" lerhard/pandoc make diff depth=5
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