#!/usr/bin/env python3
"""
BHA-S lightweight architecture checker.

This is a starter checker intended to be extended per repository. It avoids
mandatory third-party dependencies and performs conservative static checks.
"""
from __future__ import annotations

import argparse
import ast
import datetime as dt
import json
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable


@dataclass
class Finding:
    rule: str
    severity: str
    path: str
    line: int | None
    message: str


BUSINESS_RUNTIME_IMPORTS = (
    "sqlalchemy",
    "django.db",
    "requests",
    "httpx",
    "aiohttp",
    "boto3",
    "pymongo",
    "redis",
    "rclpy",
    "rclcpp",
)

PY_EXTENSIONS = {".py"}
SQL_EXTENSIONS = {".sql"}
CONFIG_NAMES = {"experiment_config.yaml", "experiment_config.yml"}


def iter_files(root: Path, suffixes: set[str] | None = None) -> Iterable[Path]:
    ignored = {".git", ".venv", "venv", "node_modules", "__pycache__", ".mypy_cache", ".pytest_cache"}
    for p in root.rglob("*"):
        if any(part in ignored for part in p.parts):
            continue
        if p.is_file() and (suffixes is None or p.suffix in suffixes):
            yield p


def rel(root: Path, path: Path) -> str:
    try:
        return str(path.relative_to(root)).replace("\\", "/")
    except ValueError:
        return str(path).replace("\\", "/")


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="ignore")


def import_names(source: str) -> list[tuple[str, int]]:
    names: list[tuple[str, int]] = []
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return names
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                names.append((alias.name, node.lineno))
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                names.append((node.module, node.lineno))
    return names


def check_shared_foundation(root: Path, findings: list[Finding]) -> None:
    base = root / "shared" / "foundation"
    if not base.exists():
        return
    for path in iter_files(base, PY_EXTENSIONS):
        for name, line in import_names(read_text(path)):
            if name == "cells" or name.startswith("cells."):
                findings.append(Finding(
                    "BHA-S-R002", "error", rel(root, path), line,
                    "shared/foundation must not import cells.*; shared foundation must remain business-independent.",
                ))


def check_domain_runtime_imports(root: Path, findings: list[Finding]) -> None:
    for path in iter_files(root, PY_EXTENSIONS):
        if "/domain/" not in rel(root, path):
            continue
        for name, line in import_names(read_text(path)):
            if name.startswith("infrastructure") or ".infrastructure" in name:
                findings.append(Finding("BHA-S-R006", "error", rel(root, path), line,
                                        "domain must not import infrastructure."))
            for banned in BUSINESS_RUNTIME_IMPORTS:
                if name == banned or name.startswith(banned + "."):
                    findings.append(Finding("BHA-S-R006", "error", rel(root, path), line,
                                            f"domain must not depend on runtime/adapter SDK import '{name}'."))


def check_deprecated(root: Path, findings: list[Finding]) -> None:
    today = dt.date.today()
    pattern = re.compile(r"@deprecated\([^\n]*expire_date\s*=\s*['\"](\d{4}-\d{2}-\d{2})['\"]")
    for path in iter_files(root, PY_EXTENSIONS):
        for idx, line in enumerate(read_text(path).splitlines(), start=1):
            match = pattern.search(line)
            if not match:
                continue
            try:
                expire_date = dt.date.fromisoformat(match.group(1))
            except ValueError:
                continue
            if expire_date < today:
                findings.append(Finding("BHA-S-R007", "warning", rel(root, path), idx,
                                        f"deprecated item expired on {expire_date.isoformat()}; remove or renew with ADR/issue."))


def check_sql_cross_join(root: Path, findings: list[Finding]) -> None:
    join_re = re.compile(r"\bjoin\b", re.IGNORECASE)
    for path in iter_files(root, SQL_EXTENSIONS):
        for idx, line in enumerate(read_text(path).splitlines(), start=1):
            if join_re.search(line) and "bha: allow-cross-cell-join" not in line:
                findings.append(Finding("BHA-S-R003", "warning", rel(root, path), idx,
                                        "SQL JOIN found. Confirm it is within one Cell; cross-Cell source table JOIN is forbidden."))


def check_experiment_config(root: Path, findings: list[Finding]) -> None:
    required_tokens = ["seed:", "dataset_version:", "git_commit:"]
    for path in iter_files(root, None):
        if path.name not in CONFIG_NAMES:
            continue
        text = read_text(path)
        for token in required_tokens:
            if token not in text:
                findings.append(Finding("BHA-S-R004", "error", rel(root, path), None,
                                        f"formal experiment config missing required field '{token[:-1]}'."))


def check_robot_control_safety(root: Path, findings: list[Finding]) -> None:
    for path in iter_files(root, PY_EXTENSIONS):
        lower_path = rel(root, path).lower()
        if "control" not in lower_path and "controller" not in lower_path:
            continue
        text = read_text(path).lower()
        if "timeout" not in text:
            findings.append(Finding("BHA-S-R005", "warning", rel(root, path), None,
                                    "robot/control path should define timeout behavior."))
        if "safety_check" not in text and "safety" not in text:
            findings.append(Finding("BHA-S-R005", "warning", rel(root, path), None,
                                    "robot/control path should call safety_check or equivalent safety guard."))


def run(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    check_shared_foundation(root, findings)
    check_domain_runtime_imports(root, findings)
    check_deprecated(root, findings)
    check_sql_cross_join(root, findings)
    check_experiment_config(root, findings)
    check_robot_control_safety(root, findings)
    return findings


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="BHA-S lightweight architecture checker")
    parser.add_argument("--root", default=".", help="project root to scan")
    parser.add_argument("--json", action="store_true", help="emit JSON")
    parser.add_argument("--fail-on-warning", action="store_true", help="treat warnings as failures")
    args = parser.parse_args(argv)

    root = Path(args.root).resolve()
    findings = run(root)

    if args.json:
        print(json.dumps([asdict(f) for f in findings], ensure_ascii=False, indent=2))
    else:
        if not findings:
            print("BHA-S check passed: no findings.")
        for f in findings:
            loc = f"{f.path}:{f.line}" if f.line else f.path
            print(f"{f.severity.upper()} {f.rule} {loc} - {f.message}")

    has_error = any(f.severity == "error" for f in findings)
    has_warning = any(f.severity == "warning" for f in findings)
    if has_error or (args.fail_on_warning and has_warning):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
