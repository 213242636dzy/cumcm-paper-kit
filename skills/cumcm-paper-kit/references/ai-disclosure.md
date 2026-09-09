# AI usage declaration and details

Use this workflow only from real usage records. Never reconstruct a fictional history after the fact.

## Paper declaration

Place `AI工具使用声明` immediately before the references.

- If no AI tool was used, state that clearly and do not attach a usage-details file.
- If AI was used, briefly list only the actual purposes and point to the support-material details file.
- Keep the short declaration consistent with the detailed ledger. Do not list tools or prompts in the reference list.

## Support-material details

Create the PDF with the exact filename `AI工具使用详情.pdf` when AI was used. It must cover:

1. tool name and version/model;
2. purpose and stage;
3. principal prompting approach and use process, with representative interactions when useful;
4. whether the output was rejected, partly adopted, or adopted;
5. manual changes and verification, except that pure language polishing need not itemize this final category.

Use sequential record IDs such as `A-01`, `A-02`, and interaction IDs such as `E-01`. The same tool, stage, and record ID must remain consistent across tables and prose.

## Evidence standard

For modeling ideas, data processing, code, validation, and result interpretation, record the concrete human check. Examples include independent formula derivation, source verification, code review, actual execution, cross-calculation, feasibility checks, residual diagnostics, sensitivity analysis, and result reproduction.

Do not use vague statements such as “checked and correct” when a real verification action can be stated. Do not claim that AI guaranteed correctness or independently completed core modeling.

## Missing information

If a required field is absent, write `待补充` and keep the submission `NO-GO`. Do not infer:

- an unrecorded model/version;
- prompts or interaction content;
- whether an output was adopted;
- manual edits or verification;
- code execution or model-test results.

## Consistency audit

Before final delivery:

- compare the paper declaration with the AI-use ledger and `AI工具使用详情.pdf`;
- confirm every substantive AI-assisted stage has a record;
- confirm outputs not adopted are not described as used in the paper;
- confirm the paper contains only manually verified results;
- remove identity, account, and private conversation metadata from the anonymous support file;
- render and inspect the details PDF.

Seed schema: `assets/ledgers/ai-usage-ledger.csv`.
