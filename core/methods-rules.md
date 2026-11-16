# Methods rules

These rules apply whenever the work reports data: survey results, interview findings, routine statistics, costs or models. In this file, `<wp>/` stands for the work package's folder. They come from a manuscript in which statistical tests were added on a self-selected sample of 89 with 20 events, at about 49% power. The tests reached the Abstract, and co-authors asked for them to be removed.

## Before any new analysis

A new analysis, an inferential test, or a change to how data are analyzed goes to the lead as a memo before it runs (`core/escalation-threshold.md`, kind 6). The memo states:

1. how the sample was drawn: random, census, purposive, self-selected or convenience;
2. the sample size, and the number of events or responses in each group compared;
3. the power or the expected precision for the effect of interest;
4. what the analysis can and cannot show, given points 1 to 3;
5. what will be reported if the result does not support the claim.

## Inference

- **Self-selected or convenience samples:** report descriptive statistics only (counts, percentages, medians and ranges). Do not report p-values, odds ratios, confidence intervals for associations, or significance language. State once in the methods why comparisons are descriptive.
- **Checking tests:** a test run to check a claim stays in the analysis notes. If it does not support the claim, retract the claim and report descriptively. Do not move the test into the abstract, results or discussion.
- **No tests "for completeness":** this includes tests by sex or by subgroup. Report subgroup figures descriptively, following the Sex and Gender Equity in Research (SAGER) guidelines.
- **Wording:** do not call a result significant, strong, a predictor or an effect unless the design supports inference. Use plain comparative wording, such as "more often" or "in this sample".

## Numbers that can be reproduced

- Every number from an analysis comes from a script in `<wp>/work/analysis/` that runs on the data. No number is typed in by hand.
- Keep a reproduction check in `<wp>/work/analysis/reproduction_check.csv`. Each row holds a number in the draft, the script's value and whether they match. When a number changes, rerun the script and update every place the number appears.
- Record the software and versions used, for the methods section.

## Qualitative findings

- A statement about participants in general needs a count from the coded data, for example "9 of 12 physicians". In one draft, "interviewed physicians" named higher pay abroad; the coded data showed only one physician had said it.
- Each count and each quotation traces to a participant code and a location in the coded data.
- A theme enters the text only after the people who coded the data have confirmed it.

## Checks

- In its draft check, the evidence checker matches each reported number against the script output or the reproduction check. It also flags inferential language these rules do not allow.
- The draft check confirms each qualitative count against the coded data.
