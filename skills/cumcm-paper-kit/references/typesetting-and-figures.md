# Word, LaTeX, tables, equations, and figures

## Choose one primary authoring route

### Word

Use `assets/templates/CUMCM-2026-论文空白模板.docx` as the writable starting document. Treat `assets/templates/2026年数学建模竞赛论文模板.docx` as a visual and instructional reference, not as a clean submission file.

- Copy the clean template to the project; never overwrite either asset.
- The supplied manual uses black for paper/template content, blue for operations, red for explanations, green for warnings, yellow for AI prompts, and gray for checklists. Never carry those colored instructions, its teaching table of contents, or prompt text into the final paper.
- Preserve the clean template's A4 page setup, 2.5 cm margins, page numbering, `CUMCM ...` style hierarchy, and caption conventions unless a current rule requires a change.
- The clean template embeds `Source Han Serif CN Regular` so arbitrary Chinese text renders without depending on a machine-local Chinese font. Keep the embedded font relationship intact when editing or converting the file.
- Use native Word equations when editability and searchability matter. Do not leave raw LaTeX strings in the document.
- After every structural change, render to page PNGs and inspect all pages at normal reading zoom.

### LaTeX

Use the project initializer to create the working LaTeX tree from `assets/templates/2026latex模板.zip`, and keep the original ZIP unchanged.

- Use the initialized working copy: it decodes the archive's Chinese filenames and removes the legacy `\tableofcontents`, blank abstract-page style, and second page-number reset that conflict with the verified 2026 baseline.
- Start from `论文.tex` and its split chapter files; do not flatten the project into one file without a reason.
- Compile with the engine expected by the class and Chinese-font configuration, normally XeLaTeX for this template.
- Keep `format.cls`, the bundled Source Han Serif CN fonts, and relative paths together.
- Replace template examples and placeholders; remove unused chapter inputs and bibliography entries.
- Compile from a clean build, inspect the log for missing fonts/references/overfull boxes, then render the PDF and inspect every page.

## Template traits to preserve

The supplied templates use an A4 contest-paper layout, Chinese serif body typography, structured headings, numbered equations/figures/tables, a dedicated abstract page, sectioned model workflow, and appendices/support-file mapping. The LaTeX asset splits content into abstract, introduction/restatement, overall analysis, assumptions, notation, model/solution, validation, evaluation, improvement/extension, references, and appendix files.

The templates are style authorities, not sources of factual content. Replace all examples with problem-specific verified work.

## Equations

- Define variables, domains, indices, and units before or immediately after the first formula.
- Use semantic operators and upright text for functions/units.
- Keep an optimization objective and all constraints visually together.
- Number equations only when referenced later.
- Check line breaks, delimiter sizing, sub/superscripts, matrices, and Chinese glyph rendering in the final PDF.
- Never turn an unverified formula into a polished graphic to disguise its status.

## Tables

- Use three-line tables for compact comparisons and result matrices when compatible with the template.
- Put units in headers; align decimal values and keep precision consistent with the problem.
- Do not repeat identical values in both a table and a figure unless each has a distinct role.
- Move long raw outputs to the appendix/support package while retaining decisive values in the body.
- In Word, allow row expansion and prevent clipped formulas or wrapped headers; in LaTeX, inspect `overfull` warnings and column widths.

## Figure decision rules

| Purpose | Preferred artifact |
|---|---|
| Quantitative evidence | Python/R/MATLAB chart generated from saved result data |
| Model/data workflow | Editable SVG, Mermaid-derived SVG, or vector drawing |
| Geometry/network/path | Programmatic plot from coordinates or graph data |
| Mechanism schematic | Editable vector diagram with explicit labels and assumptions |
| Decorative illustration | Usually omit; it consumes space without supporting a claim |

Do not use image generation for numeric charts, measured geometry, fitted curves, sensitivity plots, or diagrams whose layout encodes evidence. A generative image may be used only when the user explicitly needs a non-evidentiary illustration and it is clearly labeled as such.

## Figure style

- Use `scripts/cumcm_plot_style.py` as a baseline for Matplotlib charts.
- Match the paper's Chinese serif type; use Source Han Serif CN when available and Times New Roman or a compatible serif for Latin/math.
- Design for the available text width. Default single-column-like width is about 14--15 cm for this A4 template; verify against the actual working file.
- Export PDF/SVG for vector insertion and PNG at 300 dpi or higher for preview/fallback.
- Use a colorblind-safe, grayscale-distinguishable palette; add line styles/markers/hatching when color alone is insufficient.
- Avoid chart titles that duplicate captions. Put a concise claim-driven caption in the paper.
- Label axes with quantity and unit, show uncertainty when relevant, and do not truncate axes in a misleading way.
- Use consistent model names, colors, symbols, precision, and ordering across figures and tables.

## Figure-text integration

For every figure, record:

1. the question or claim it addresses;
2. source data and generating command;
3. visual encodings and units;
4. the one-sentence caption claim;
5. the body sentence before it and the interpretation after it;
6. uncertainty, limitations, or conditions not visible in the graphic.

Render at final insertion size. Check Chinese glyphs, line weights, legends, subfigure labels, raster sharpness, and caption/page breaks.
