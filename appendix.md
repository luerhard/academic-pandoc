
```{=latex}
\newpage
```
```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

# References {.unnumbered}
::: {#refs}
:::
\newpage

```{=latex}
\newpage
```
```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```
::::: {.appendix}
# Appendices {.unnumbered}

# Introduction to the Appendix {#ap:super_important}

There is only unnecessary stuff in those appendices which just exists we can reference stuff in the main part. (For now).

![And another cat](rsc/images/cat.jpg){#fig:catpic_A width=75%}

This is my appendix

```{.table #tbl:desc}
---
alignment: LLL
caption: Example Table from csv
width: [0.2,0.2,0.2]
include: rsc/tables/sample.csv
markdown: true
---
```

# New appendix {#ap:B}

My super important descriptives! I want to cite here: @blumenau:NeverLetGood.2018

![A cat in the appendix](rsc/images/cat.jpg){#fig:catpic_B_small width=5%}

## Subappendix {#ap:subappendix}

```{.table #tbl:subap}
---
alignment: LLL
caption: Example Table from csv
width: [0.2,0.2,0.2]
include: rsc/tables/sample.csv
markdown: true
---
```

### subsubappendix {#ap:subsub}

```{.table #tbl:subsubap}
---
alignment: LLL
caption: Example Table from csv
width: [0.2,0.2,0.2]
include: rsc/tables/sample.csv
markdown: true
---
```

![A cat in the appendix](rsc/images/cat.jpg){#fig:catpic_B width=75%}
:::::
