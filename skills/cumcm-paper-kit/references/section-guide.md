# Section guide

Read only the sections relevant to the current task. Preserve the template's actual numbering when it differs from this guide.

## Title, abstract, and keywords

Write these after the final body and results are fixed.

- Title: name the research object and the principal modeling idea without stacking every algorithm.
- Opening: one short background sentence and one sentence defining the problem scope.
- Main body: normally one paragraph per subproblem. State the task, essential processing/assumption, model and mathematical type, solver, key quantitative answer, and matching validation.
- Closing: only real innovations, verified strengths, limitations, and a bounded application scope.
- Keywords: usually 4--6 covering the problem, principal model, and core algorithm/innovation.
- No formulas, figures, tables, citation numbers, unexplained abbreviations, or fabricated validation in the abstract.

## Problem restatement

- Separate background from required tasks.
- Rewrite rather than copying large portions of the prompt.
- Retain essential values, units, conditions, output format, and precision.
- Make subproblem dependencies explicit without forcing a sequential relationship that the prompt does not contain.
- Keep solution methods and final results out of this section.

## Problem analysis

Answer: what must be solved, what mathematical structure each task has, how tasks interact, what data issues matter, why the selected route fits, how it will be validated, and what must be delivered.

This section may describe planned preprocessing and model families, but it must not contain fabricated data characteristics, calculated results, or a full derivation duplicated from later sections.

## Model assumptions

Each assumption states:

1. the condition being assumed;
2. why it is defensible for this problem;
3. which model or simplification uses it;
4. how violation affects conclusions or will be tested.

Distinguish prompt facts from team assumptions. Avoid empty claims such as “data are accurate” without a source or diagnostic.

## Notation

- Include recurring global variables, parameters, sets, indices, vectors, matrices, and units.
- Keep temporary local symbols next to the formula where they appear.
- One symbol has one meaning; one quantity keeps one symbol.
- Define domain, index range, vector/matrix styling, and unit.
- Reintroduce important symbols briefly at first body use even if they appear in the notation table.

## Model establishment and solution

For each subproblem:

1. State the task, inputs, output, mathematical type, and model choice rationale.
2. Describe only the preprocessing actually performed and preserve its parameters.
3. Define variables and parameters before the equation.
4. Present the objective/core equations, all constraints, domains, and boundary/initial conditions together.
5. Trace parameter values to problem facts, data estimates, literature, or declared assumptions.
6. Explain the algorithm, initialization, settings, stopping condition, software/environment, and failure status.
7. Present the requested result, interpret it, compare it fairly, and attach the relevant validation.

For optimization, recheck feasibility after rounding. For forecasting, prevent time/data leakage and compare a simple baseline. For evaluation/ranking, explain indicator direction, normalization, and weight source and test ranking stability. For simulation or randomized search, record seeds and repeated-run uncertainty.

## Results, validation, and sensitivity

- Use metrics that match the claim and problem type.
- Report units, denominators, sample sizes, uncertainty, and comparison conditions.
- Distinguish in-sample fit from out-of-sample prediction.
- Sensitivity parameters must be important or uncertain; vary justified ranges and state whether conclusions, not only raw values, remain stable.
- A failed diagnostic is evidence to narrow the claim or revise the model, not something to hide.

## Model evaluation, improvement, and extension

- Tie each strength to a concrete design choice or metric.
- Tie each limitation to its source, consequence, and applicability boundary.
- Map every proposed improvement to a stated limitation and a feasible validation test.
- Explain what stays invariant and what changes when extending the model to another context.
- Do not repeat the abstract or all numerical results.

## References and appendix

- Cite at first substantive use of an external method, formula, data source, standard, or public claim.
- Every in-text citation maps to one real, verified reference; every listed reference is used.
- Do not list AI tools as references; handle them in the AI-use disclosure.
- Appendix and support manifest contain all complete runnable code or interactive commands required for reproduction.
- Keep principal equations, key results, and decisive validation in the body. The appendix supplements; it does not hide the answer.
- Remove personal paths, account names, document metadata, school/team identity, and secrets from paper, code, figures, filenames, archives, and logs.
