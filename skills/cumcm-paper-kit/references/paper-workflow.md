# Paper and evidence workflow

## Intake packet

Inventory each item and label it `provided`, `generated`, `missing`, `unreadable`, or `not-applicable`:

- official problem statement and output templates;
- attachments, field definitions, units, time/space ranges, and precision requirements;
- raw and processed data;
- source code, environment, parameters, seeds, commands, and logs;
- result tables, figures, metrics, feasibility checks, and sensitivity outputs;
- literature and external-data sources;
- existing paper draft and target Word/LaTeX template;
- AI usage records;
- regional/school notice and submission constraints.

Do not draft around a missing attachment as if it were absent from the problem. State what cannot yet be checked.

## Five ledgers

Create only those needed by the task. Seed files are in `assets/ledgers/`.

1. **Claim-evidence ledger**: each result or evaluative claim points to a result file, code command, validation output, or citation.
2. **Figure ledger**: figure ID, question answered, source data, generating script, export files, caption claim, and body anchor.
3. **Symbol ledger**: symbol, meaning, unit, domain, first use, and model ownership.
4. **Citation ledger**: source, claim supported, body location, access/DOI, and verification status.
5. **AI-use ledger**: tool/model, real purpose, prompt summary, output, adoption, manual change, verification, and evidence path.

## Subproblem contract

For each subproblem record:

| Field | Required content |
|---|---|
| Task | The decision, estimate, classification, explanation, or design requested |
| Inputs | Files, fields, units, upstream results, and assumptions |
| Model | Variables, parameters, objective/equations, constraints, and rationale |
| Solver | Algorithm, configuration, seed, stopping rule, and environment |
| Outputs | Exact table/figure/value/plan required by the problem |
| Validation | Baseline, metric, feasibility, uncertainty, sensitivity, or independent check |
| Paper map | Section, equations, figures/tables, result sentence, appendix/support files |
| Status | verified, pending, failed, or out-of-scope |

Upstream uncertainty must propagate into downstream claims when subproblems depend on one another.

## Build sequence

1. Read the problem and attachments; freeze the subproblem contract.
2. Preserve raw data and create reproducible transformations.
3. Establish an interpretable baseline before a more complex main model.
4. Run the model and save machine-readable outputs before writing result prose.
5. Validate claims with tests matched to the model type.
6. Generate figures from saved outputs, not from manually typed values.
7. Draft the model/result body, then introduction/analysis, then evaluation, and the abstract last.
8. Reconcile symbols, units, model names, numbers, figure/table IDs, citations, appendix files, and AI disclosures.
9. Render and visually inspect every page.
10. Run the preflight audit and keep `NO-GO` until blockers are resolved.

## Suggested project tree

```text
problem/              official statement and read-only attachments
data/raw/             immutable input data
data/processed/       reproducible derived data
src/                  runnable analysis/model/figure code
outputs/tables/       machine-readable results
outputs/figures/      PDF/SVG plus PNG previews
paper/                Word or LaTeX source and final PDF
support/              files intended for the support archive
ledgers/              claim, figure, symbol, citation, and AI-use ledgers
logs/                 commands, environment, solver, and run records
submission/           final paper and support archive only
```

Use `scripts/init_cumcm_project.py TARGET --format word|latex` to create this structure without overwriting existing files.

## Stop conditions

- Do not write final numeric prose until the output is produced and checked.
- Do not declare global optimality without solver or proof evidence.
- Do not declare robustness from one arbitrary perturbation.
- Do not submit while placeholders, identity leaks, missing code, broken references, inconsistent AI records, or visual defects remain.
