---
name: BHA-S Engineering Skill V1.0
description: Use this skill when designing, implementing, reviewing, refactoring, or validating software, algorithm, AI-tooling, or robotics engineering projects with BHA-S: Scalable Bionic Homeostasis Architecture. This skill turns architecture work into executable rules, templates, checks, and evidence collection.
version: 1.0
---

# BHA-S Engineering Skill V1.0

## Purpose

Use this skill to make Codex build and modify projects according to **BHA-S: Scalable Bionic Homeostasis Architecture**. BHA-S is a meta-architecture engineering system: it uses system homeostasis as the target, autonomous cells as capability boundaries, explicit contracts as membranes, typed signals as collaboration semantics, immune/recovery rules for failure handling, rhythm/evolution rules for delivery, and evidence collection to prove whether the system remains healthy.

This skill is not a naming gimmick and does not require microservices. Start with the smallest project shape that preserves boundaries and evidence.

## When to use

Use this skill when the user asks to:

- design a new project architecture;
- create a maintainable personal tool or company business system;
- build an AI coding, automation, audit, or LLM tool platform;
- design algorithm engineering, MLOps, experiment, or model deployment projects;
- design robotics, ROS, edge-agent, perception/planning/control, or robot-cloud systems;
- refactor an existing project to reduce coupling and code rot;
- review a codebase for boundary violations, shared-layer pollution, hard-coded configuration, architecture debt, or AI-generated code risks;
- generate project scaffolds, cells, cluster maps, contracts, architecture docs, tests, or checking scripts.

## Non-negotiable operating loop

Before editing code, follow this loop and show a concise decision summary to the user:

1. **Scale classification**: classify the project as L1, L2, L3, or L4.
2. **Intent classification**: classify the request as Command, Query, Event, Metric, Job, UI, Experiment, Model, ROS Node, Hardware Adapter, or Documentation.
3. **Cell placement**: identify the target Cell and Cluster from `architecture/cell-map.md` or propose a new Cell with justification.
4. **Impact analysis**: list contracts, events, read models, owned data, tests, evidence metrics, and docs that may change.
5. **Risk analysis**: check transaction consistency, idempotency, concurrency, data loss, safety level, model reproducibility, runtime failure, and rollback.
6. **Vertical slice first**: implement the smallest working end-to-end slice before widening abstractions.
7. **Run checks**: run tests and BHA-S checks where possible; if checks are unavailable, add or update the check configuration.
8. **Evidence update**: update generated evidence, changelog, ADR, or validation notes for architecture-significant changes.

## Required project scale behavior

- **L1 script**: keep it simple. Require config externalization, basic logging, error handling, and no hard-coded secrets.
- **L2 personal tool / small app**: use modular monolith, core Cells, in-process EventBus when useful, structured logs, task state, retry/fallback for external calls, and basic architecture checks.
- **L3 company system**: use Cell Clusters, owned data, API/event contracts, database migrations, permissions, shared-layer entry criteria, consistency model, CI checks, ADRs, and automated evidence.
- **L4 platform / distributed / robotics safety-critical system**: enforce contracts, service/database isolation, distributed tracing, error budgets, rollback playbooks, Saga/TCC/Outbox/Inbox, security scans, safety case, and stronger CI blocking rules.

## Canonical project artifacts

When creating or upgrading a BHA-S project, prefer these artifacts:

```text
architecture/
  homeostasis.md
  cell-map.md
  ownership.md
  signal-map.md
  consistency-model.md
  evolution-matrix.md
  fitness.md
  evidence.md
  decisions/
  diagrams/
contracts/
  openapi/
  asyncapi/
  schemas/
  examples/
templates/
tests/
  unit/
  integration/
  contract/
  architecture/
bha.yaml
```

## Standard Cell structure

Use this structure unless the project scale justifies a lighter one:

```text
cells/<cluster>/<cell>/
  README.md
  interfaces/                  # inbound adapters: HTTP/CLI/UI/ROS service servers
  application/
    services/
    commands/
    queries/
    ports/                     # application-owned port interfaces
  domain/                      # entities, value objects, policies, invariants
  infrastructure/
    adapters/
      database/
      external_api/
      model_client/
      hardware/
      anti_corruption/
  events/
  jobs/
  observability/
  tests/
```

For L2 soft-cluster migration, the physical path may remain `cells/<cell>/` while `bha.yaml` and `architecture/cell-map.md` declare logical Cluster ownership.

## Data ownership and database boundary rules

- Every business datum has exactly one authoritative owner Cell.
- Other Cells must read through Query API, Read Model, event projection, materialized view, or reporting/query center.
- Same-Cell internal JOINs are allowed.
- Cross-Cell **source table JOINs are forbidden** unless explicitly waived with an ADR-bound temporary exception.
- Cross-Cell writes are forbidden except through public Command/Application facade.
- L3/L4 should use separate database schemas or instances for Cell/Cluster boundaries when feasible.

## Shared layer entry criteria

Only allow these in `shared/`:

- pure computation utilities without business vocabulary;
- protocol-neutral primitives;
- logging, metrics, tracing, error base classes;
- test fixtures and framework glue with no business logic.

Never put domain rules, status transitions, business policies, or Cell-specific adapters in `shared/`.

## Signal and consistency rules

- **Command**: request to change state; must be intentional and idempotency-aware.
- **Query**: read request; must declare freshness and consistency needs.
- **Event**: fact that already happened; use past-tense names such as `AuditCompleted`.
- **Metric**: observable signal; never use logs/metrics as business state.

Consistency levels:

- **C0**: single-Cell consistency.
- **C1**: same deployment/local transaction consistency.
- **C2**: cross-Cell eventual consistency through events/read models.
- **C3**: distributed consistency through Saga/TCC/Outbox/Inbox/idempotent consumers.

## AI hard constraints

Never do these:

1. Put business state-transition logic inside `infrastructure/adapters`.
2. Let `shared/foundation` import `cells.*` or depend on business Cells.
3. Let a RabbitMQ/Kafka/Topic consumer directly connect to another Cell's database.
4. Omit `seed`, `dataset_version`, or `git_commit` for formal algorithm experiments.
5. Omit `timeout`, `safety_check`, or emergency-stop/safe-state handling in robot control paths.
6. Modify contracts without updating contract tests and compatibility notes.
7. Bypass `application`/facade to mutate another Cell's domain state.
8. Leak external DTOs, SDK objects, status codes, or external exceptions into `domain`.

## Algorithm engineering profile

For algorithm projects, add these Cells or equivalents:

```text
algorithm_cluster/
  dataset_manager
  data_pipeline
  experiment_runner
  algorithm_policy
  algorithm_kernel
  evaluator
  model_registry
  inference_service
  monitoring
  report_generator
```

Rules:

- Formal experiments require `ExperimentConfig` snapshot.
- Track `seed`, `dataset_version`, `dataset_hash`, `git_commit`, `config_version`, `environment`, and metric definitions.
- `algorithm_policy` describes objectives, constraints, rewards, metrics, and evaluation rules.
- `algorithm_kernel` may depend on PyTorch/JAX/TensorFlow; do not over-abstract compute kernels into unreadable architecture purity.
- Deployed models must be versioned, reproducible, monitorable, and rollbackable.

## Robotics engineering profile

For robotics/ROS projects, add these Cells or equivalents:

```text
robot_cluster/
  perception
  localization
  planning
  control
  manipulation
  safety_guard
  hardware_adapter
  simulator
  telemetry
  task_executor
```

Rules:

- Hard real-time control loops must not depend on remote services.
- Safety-critical nodes must support controlled lifecycle or equivalent lifecycle wrapper.
- Map BHA-S Command to ROS Service/Action, Event to Topic, Query to Service/local state, Metric to diagnostics/telemetry.
- One BHA-S Cell may contain multiple ROS Nodes; do not split high-frequency paths into excessive nodes for architectural neatness.
- Define Safety Level S0-S3 and enforce stronger timeout, safety_check, safe_state, emergency stop, HIL, and safety-case rules for S2/S3.

## Architecture checks

When possible, use or extend `tools/bha_check.py`. Checks should report rule IDs such as:

- `BHA-S-R001`: no cross-Cell direct state mutation.
- `BHA-S-R002`: `shared/foundation` must not import `cells.*`.
- `BHA-S-R003`: no cross-Cell source table JOIN.
- `BHA-S-R004`: formal experiments require seed/dataset_version/git_commit.
- `BHA-S-R005`: robot control paths require timeout and safety_check.
- `BHA-S-R006`: no domain dependency on infrastructure/HTTP/DB/SDK/ROS runtime.
- `BHA-S-R007`: deprecated code past expiry must not remain in active use.

Use severity by level:

- L2: limited Errors, most style rules Warning.
- L3: core boundaries and contracts Error.
- L4/S2/S3: safety, contracts, data boundaries, and runtime resilience are Error.

## Output expectations

When using this skill, output:

1. scale level;
2. target Cell/Cluster;
3. files changed or proposed;
4. contracts/events/data/read models affected;
5. risks and mitigation;
6. checks run and results;
7. remaining architecture debt, if any.

## Supporting documents

Use these files in this skill package:

- `docs/BHA-S_ENGINEERING_SPEC_V1.0.md` — full engineering specification.
- `templates/bha.yaml` — configurable architecture rules.
- `templates/architecture/*` — starter docs.
- `templates/algorithm/experiment_config.yaml` — experiment reproducibility template.
- `templates/robotics/*` — ROS mapping and safety templates.
- `tools/bha_check.py` — lightweight architecture checker starter.
