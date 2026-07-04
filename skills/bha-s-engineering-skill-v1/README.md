# BHA-S Engineering Skill V1.0

This is a Codex-ready skill package for **BHA-S: Scalable Bionic Homeostasis Architecture**.

## Package structure

```text
SKILL.md                      # Codex skill entry point
docs/                         # Full specification and operating manual
templates/                    # Project templates and architecture docs
tools/                        # Lightweight checkers and automation starters
examples/                     # Minimal examples
```

## Recommended usage

1. Let Codex load this skill.
2. Ask Codex to classify the target project as L1/L2/L3/L4.
3. Generate or update `bha.yaml` and `architecture/cell-map.md`.
4. Implement one vertical slice first.
5. Run `python tools/bha_check.py --root <project-root>`.
6. Use generated check results as part of architecture evidence.

## Maturity status

This package is named **V1.0** because it is the first mature Codex-integrable package. The underlying engineering specification consolidates the previous BHA-S v1.2 rule set.
