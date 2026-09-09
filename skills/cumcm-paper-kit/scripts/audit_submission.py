#!/usr/bin/env python3
"""Deterministic preflight checks for a CUMCM paper and support archive."""

from __future__ import annotations

import argparse
import json
import re
import sys
import zipfile
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable
from xml.etree import ElementTree


MAX_BYTES = 20 * 1024 * 1024
TEXT_SUFFIXES = {".txt", ".md", ".tex", ".csv"}
SOURCE_SUFFIXES = {
    ".py", ".m", ".r", ".jl", ".c", ".cpp", ".java", ".ipynb", ".xlsx", ".xls", ".sav", ".sps",
}
PLACEHOLDER_PATTERNS = (
    r"【[^】]*(?:待补充|填写|模型名称|关键|具体|问题[一二三四1234xX])[^】]*】",
    r"\b(?:TODO|TBD|FIXME)\b",
    r"(?:待补充|待核验)",
)
GENERIC_IDENTITY_PATTERNS = (
    "参赛者姓名", "队员姓名", "学校名称", "所在学校", "学院", "学号", "指导教师", "参赛队号", "赛区",
)
REQUIRED_AI_DETAIL_MARKERS = (
    ("工具名称", "工具名"),
    ("版本", "型号", "模型"),
    ("使用目的", "具体用途", "使用环节"),
    ("提示", "交互"),
    ("采纳",),
    ("人工修改", "修改情况"),
    ("核验", "验证"),
)


@dataclass
class Finding:
    severity: str
    code: str
    message: str
    evidence: str = ""


@dataclass
class DocumentView:
    path: Path
    text: str
    first_page: str
    pages: int | None
    metadata: dict[str, str]
    warnings: list[str]


def decode_text(data: bytes) -> str:
    for encoding in ("utf-8-sig", "utf-8", "gb18030"):
        try:
            return data.decode(encoding)
        except UnicodeDecodeError:
            continue
    return data.decode("utf-8", errors="replace")


def extract_docx(path: Path) -> DocumentView:
    warnings: list[str] = []
    metadata: dict[str, str] = {}
    with zipfile.ZipFile(path) as archive:
        root = ElementTree.fromstring(archive.read("word/document.xml"))
        chunks: list[str] = []
        for element in root.iter():
            if element.tag.endswith("}t") and element.text:
                chunks.append(element.text)
            elif element.tag.endswith("}p"):
                chunks.append("\n")
        if "docProps/core.xml" in archive.namelist():
            core = ElementTree.fromstring(archive.read("docProps/core.xml"))
            for element in core.iter():
                if element.text and element.tag.rsplit("}", 1)[-1] in {"creator", "lastModifiedBy", "title"}:
                    metadata[element.tag.rsplit("}", 1)[-1]] = element.text.strip()
    text = "".join(chunks)
    return DocumentView(path, text, text[:5000], None, metadata, warnings)


def extract_pdf(path: Path) -> DocumentView:
    warnings: list[str] = []
    try:
        from pypdf import PdfReader
    except ImportError:
        return DocumentView(path, "", "", None, {}, ["pypdf is unavailable; PDF text and page checks were skipped"])

    reader = PdfReader(path)
    page_texts: list[str] = []
    for page in reader.pages:
        try:
            page_texts.append(page.extract_text() or "")
        except Exception as exc:  # damaged or image-only pages
            warnings.append(f"page text extraction failed: {exc}")
            page_texts.append("")
    metadata = {}
    if reader.metadata:
        for key, value in reader.metadata.items():
            if value:
                metadata[str(key)] = str(value)
    return DocumentView(path, "\n".join(page_texts), page_texts[0] if page_texts else "", len(reader.pages), metadata, warnings)


def read_document(path: Path) -> DocumentView:
    suffix = path.suffix.lower()
    if suffix == ".docx":
        return extract_docx(path)
    if suffix == ".pdf":
        return extract_pdf(path)
    if suffix in TEXT_SUFFIXES:
        text = decode_text(path.read_bytes())
        return DocumentView(path, text, text[:5000], None, {}, [])
    raise ValueError(f"Unsupported paper format: {suffix}")


def archive_entries(path: Path) -> tuple[list[str], list[str]]:
    warnings: list[str] = []
    if path.suffix.lower() == ".zip":
        with zipfile.ZipFile(path) as archive:
            return archive.namelist(), warnings
    if path.suffix.lower() == ".rar":
        try:
            import rarfile
        except ImportError:
            return [], ["rarfile is unavailable; RAR entries were not inspected"]
        with rarfile.RarFile(path) as archive:
            return archive.namelist(), warnings
    return [], ["support package must be a .zip or .rar file"]


def normalize(text: str) -> str:
    return re.sub(r"\s+", "", text).lower()


def contains_any(text: str, values: Iterable[str]) -> bool:
    compact = normalize(text)
    return any(normalize(value) in compact for value in values)


def add(findings: list[Finding], severity: str, code: str, message: str, evidence: str = "") -> None:
    findings.append(Finding(severity, code, message, evidence[:300]))


def check_size(path: Path, role: str, findings: list[Finding]) -> None:
    size = path.stat().st_size
    if size > MAX_BYTES:
        add(findings, "BLOCKER", "FILE_SIZE", f"{role} exceeds 20 MiB", f"{path}: {size} bytes")
    else:
        add(findings, "INFO", "FILE_SIZE", f"{role} size is within 20 MiB", f"{size} bytes")


def check_paper(view: DocumentView, identity_terms: list[str], findings: list[Finding]) -> bool | None:
    text = view.text
    compact = normalize(text)

    for warning in view.warnings:
        add(findings, "WARN", "EXTRACTION", warning, str(view.path))
    if not text.strip():
        add(findings, "WARN", "NO_TEXT", "No paper text could be extracted; perform manual visual inspection", str(view.path))

    for pattern in PLACEHOLDER_PATTERNS:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            add(findings, "BLOCKER", "PLACEHOLDER", "Paper contains an unresolved placeholder", match.group(0))
            break

    for term in identity_terms:
        if term and (normalize(term) in compact or normalize(term) in normalize(view.path.name)):
            add(findings, "BLOCKER", "IDENTITY_TERM", "Paper content or filename contains a user-specified identity term", term)

    for pattern in GENERIC_IDENTITY_PATTERNS:
        if normalize(pattern) in compact:
            add(findings, "WARN", "IDENTITY_REVIEW", "Potential identity-related text requires manual review", pattern)

    application_names = ("wps", "microsoft", "word", "libreoffice", "latex", "pdftex", "xelatex")
    for key, value in view.metadata.items():
        if (
            key.lower() in {"creator", "lastmodifiedby", "/author", "/creator"}
            and value.strip()
            and not contains_any(value, application_names)
        ):
            add(findings, "WARN", "METADATA_IDENTITY", "Document metadata may reveal identity", f"{key}={value}")

    early = normalize(view.first_page or text[:6000])
    if "目录" in early:
        add(findings, "BLOCKER", "TABLE_OF_CONTENTS", "Electronic paper appears to contain a table of contents", "目录")
    if view.path.suffix.lower() == ".pdf":
        if "摘要" not in early:
            add(findings, "BLOCKER", "FIRST_PAGE", "PDF first page does not appear to be the abstract page")
        if "承诺书" in early or "编号专用页" in early:
            add(findings, "BLOCKER", "FIRST_PAGE", "Electronic paper includes a commitment or numbering page")
        if view.pages and view.pages > 30:
            add(findings, "WARN", "PAGE_COUNT", "PDF has more than 30 total pages; manually verify the body ends by page 30 and later pages are appendix", str(view.pages))

    declaration_index = compact.find("ai工具使用声明")
    reference_index = compact.find("参考文献")
    if declaration_index < 0:
        add(findings, "BLOCKER", "AI_DECLARATION", "Paper is missing the AI tool usage declaration")
        ai_used: bool | None = None
    else:
        if reference_index >= 0 and declaration_index > reference_index:
            add(findings, "BLOCKER", "AI_DECLARATION_ORDER", "AI tool usage declaration must appear before references")
        no_ai = contains_any(text[declaration_index:], ("未使用任何AI工具", "未使用AI工具"))
        used_ai = contains_any(text[declaration_index:], ("使用了AI工具", "使用AI工具"))
        if no_ai:
            ai_used = False
        elif used_ai:
            ai_used = True
        else:
            ai_used = None
            add(findings, "BLOCKER", "AI_DECLARATION_AMBIGUOUS", "AI declaration does not clearly state whether AI was used")

    if "参考文献" not in compact:
        add(findings, "WARN", "REFERENCES", "No references heading was detected")
    if "附录" not in compact and not contains_any(text, ("本论文没有用到程序", "本论文没有支撑材料")):
        add(findings, "WARN", "APPENDIX", "No appendix or explicit no-program/no-support statement was detected")

    return ai_used


def check_ai_details(path: Path, findings: list[Finding]) -> None:
    if path.name != "AI工具使用详情.pdf":
        add(findings, "BLOCKER", "AI_DETAILS_NAME", "AI usage details must use the exact filename AI工具使用详情.pdf", path.name)
    if path.suffix.lower() != ".pdf":
        add(findings, "BLOCKER", "AI_DETAILS_FORMAT", "AI usage details must be a PDF", str(path))
        return
    check_size(path, "AI usage details", findings)
    view = extract_pdf(path)
    for warning in view.warnings:
        add(findings, "WARN", "AI_DETAILS_EXTRACTION", warning)
    compact = normalize(view.text)
    substantive_terms = ("建模", "数据处理", "程序", "代码", "模型检验", "结果分析", "图表", "文献检索", "摘要")
    marker_groups = REQUIRED_AI_DETAIL_MARKERS
    if contains_any(view.text, ("语言润色",)) and not contains_any(view.text, substantive_terms):
        marker_groups = REQUIRED_AI_DETAIL_MARKERS[:4]
    for alternatives in marker_groups:
        if not any(normalize(marker) in compact for marker in alternatives):
            add(findings, "BLOCKER", "AI_DETAILS_FIELD", "AI usage details appear to miss a required field", "/".join(alternatives))
    if contains_any(view.text, ("待补充", "待核验")):
        add(findings, "BLOCKER", "AI_DETAILS_PLACEHOLDER", "AI usage details contain unresolved fields")


def check_support(path: Path, identity_terms: list[str], ai_used: bool | None, findings: list[Finding]) -> None:
    check_size(path, "Support package", findings)
    if path.suffix.lower() not in {".zip", ".rar"}:
        add(findings, "BLOCKER", "SUPPORT_FORMAT", "Support package must be one ZIP or RAR file", str(path))
        return
    entries, warnings = archive_entries(path)
    for warning in warnings:
        add(findings, "WARN", "ARCHIVE_READ", warning)
    if not entries:
        return

    joined = "\n".join(entries)
    for term in identity_terms:
        if term and normalize(term) in normalize(joined):
            add(findings, "BLOCKER", "ARCHIVE_IDENTITY", "Support archive path contains a user-specified identity term", term)
    if any(re.search(r"(?:^|/)(?:users|home)/", name, flags=re.IGNORECASE) for name in entries):
        add(findings, "WARN", "ARCHIVE_ABSOLUTE_PATH", "Archive appears to contain an absolute user path")
    if contains_any(joined, ("承诺书", "编号专用页")):
        add(findings, "BLOCKER", "ARCHIVE_FORBIDDEN", "Support archive includes a commitment or numbering page")

    source_count = sum(Path(name).suffix.lower() in SOURCE_SUFFIXES for name in entries)
    if source_count == 0:
        add(findings, "WARN", "SOURCE_CODE", "No common source-code or interactive-command file was detected in the support archive")
    else:
        add(findings, "INFO", "SOURCE_CODE", "Source-like files detected in support archive", str(source_count))

    has_ai_details = any(Path(name).name == "AI工具使用详情.pdf" for name in entries)
    if ai_used is True and not has_ai_details:
        add(findings, "BLOCKER", "AI_DETAILS_ARCHIVE", "AI was declared but AI工具使用详情.pdf is missing from the support archive")
    if ai_used is False and has_ai_details:
        add(findings, "BLOCKER", "AI_DECLARATION_MISMATCH", "Paper declares no AI use but the archive contains AI工具使用详情.pdf")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit a CUMCM electronic paper and support package")
    parser.add_argument("--paper", type=Path, required=True, help="Final PDF, DOCX, TEX, MD, or TXT paper")
    parser.add_argument("--support", type=Path, help="Final ZIP or RAR support package")
    parser.add_argument("--ai-details", type=Path, help="AI工具使用详情.pdf before it is packed")
    parser.add_argument("--identity-term", action="append", default=[], help="Exact private term to block; repeatable")
    parser.add_argument("--json-out", type=Path, help="Optional JSON report path")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    paper = args.paper.expanduser().resolve()
    if not paper.is_file():
        print(f"Paper not found: {paper}", file=sys.stderr)
        return 2

    findings: list[Finding] = []
    check_size(paper, "Paper", findings)
    try:
        view = read_document(paper)
    except Exception as exc:
        print(f"Cannot read paper: {exc}", file=sys.stderr)
        return 2
    ai_used = check_paper(view, args.identity_term, findings)

    details = args.ai_details.expanduser().resolve() if args.ai_details else paper.parent / "AI工具使用详情.pdf"
    if ai_used is True:
        if details.is_file():
            check_ai_details(details, findings)
        else:
            add(findings, "BLOCKER", "AI_DETAILS_MISSING", "AI was declared but AI工具使用详情.pdf was not provided")
    elif ai_used is False and details.is_file():
        add(findings, "BLOCKER", "AI_DECLARATION_MISMATCH", "Paper declares no AI use but AI工具使用详情.pdf exists")

    if args.support:
        support = args.support.expanduser().resolve()
        if not support.is_file():
            add(findings, "BLOCKER", "SUPPORT_MISSING", "Support package was specified but not found", str(support))
        else:
            check_support(support, args.identity_term, ai_used, findings)
    elif ai_used is True:
        add(findings, "BLOCKER", "SUPPORT_MISSING", "AI was used, so a support package containing AI工具使用详情.pdf is required")
    else:
        add(findings, "WARN", "SUPPORT_NOT_CHECKED", "No support package was provided for audit")

    blockers = sum(item.severity == "BLOCKER" for item in findings)
    warnings = sum(item.severity == "WARN" for item in findings)
    status = "NO-GO" if blockers else "GO"
    report = {
        "status": status,
        "paper": str(paper),
        "blockers": blockers,
        "warnings": warnings,
        "findings": [asdict(item) for item in findings],
    }

    print(f"Submission decision: {status}")
    print(f"Blockers: {blockers}; warnings: {warnings}")
    for item in findings:
        evidence = f" | {item.evidence}" if item.evidence else ""
        print(f"[{item.severity}] {item.code}: {item.message}{evidence}")

    if args.json_out:
        output = args.json_out.expanduser().resolve()
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"JSON report: {output}")
    return 1 if blockers else 0


if __name__ == "__main__":
    raise SystemExit(main())
