# BHA-S Engineering Skill V1.0 Specification

## 1. Positioning

BHA-S means **Scalable Bionic Homeostasis Architecture**. It is a meta-architecture engineering system for long-lived software, algorithm, AI-tooling, and robotics projects. It does not replace DDD, Clean Architecture, Hexagonal Architecture, microservices, SRE, DevOps, MLOps, or ROS. It organizes their useful practices around one target: **system homeostasis**.

A BHA-S project is healthy when it can remain understandable, changeable, recoverable, measurable, and evolvable under requirement change, dependency failure, AI-generated code, team handoff, and scale growth.

## 2. Three operating views

### Development view

Use this view when writing code.

- Cell and Cluster boundaries.
- Membrane contracts.
- Command / Query / Event / Metric semantics.
- Data ownership and Read Model rules.
- Consistency model.

### Runtime view

Use this view when operating the system.

- Timeout, retry, fallback, circuit breaker.
- Task recovery and rollback.
- Logging, metrics, traces, progress, health checks.
- CI/CD, scheduled jobs, cleanup, deployment rhythm.

### Governance view

Use this view when reviewing or evolving the system.

- Project scale level.
- Architecture fitness functions.
- Evidence layer.
- Evolution decision matrix.
- ADR and ownership.
- Deprecation and metabolism policy.

## 3. Scale levels

| Level | Use case | Minimum BHA-S requirement |
|---|---|---|
| L1 | Script / one-off tool | Config externalization, logging, error handling, no hard-coded secrets |
| L2 | Personal tool / small app | Modular monolith, core Cells, basic checks, task state, structured logs |
| L3 | Company business system | Cell Clusters, owned data, contracts, DB migration, permission, ADR, CI checks |
| L4 | Platform / distributed / safety-critical | Service/database isolation, tracing, SLO/error budget, Saga/TCC/Outbox, rollback, security/safety checks |

## 4. Cell and Cluster rules

A Cell is an autonomous capability boundary. A Cluster is a group of related Cells.

A module should become a Cell when it has at least three of these:

1. independent business or engineering purpose;
2. independent state or data ownership;
3. independent change reason;
4. explicit input/output contract;
5. possible future replacement, reuse, scaling, or service extraction.

L2 may use flat `cells/`. L3 should use Cell Cluster. During migration from L2 to L3, soft-cluster mode is allowed: physical paths remain flat while `bha.yaml` and `architecture/cell-map.md` declare logical Cluster ownership.

## 5. Standard Cell structure

```text
cells/<cluster>/<cell>/
  README.md
  interfaces/
  application/
    services/
    commands/
    queries/
    ports/
  domain/
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

`domain/` owns invariants and business rules. `application/` owns use-case orchestration. `interfaces/` owns inbound adapters. `infrastructure/adapters/` owns outbound external technology. `anti_corruption/` maps external DTOs, status codes, and exceptions into internal types.

## 6. Shared layer entry criteria

`shared/` is a governed area, not a dumping ground.

Allowed:

- pure utilities;
- protocol-neutral primitives;
- logging/metrics/tracing base wrappers;
- base error types;
- testing fixtures with no business rules.

Forbidden:

- business status transition;
- domain policies;
- Cell-specific adapters;
- functions that mention business vocabulary and change when business rules change;
- imports from `cells.*` inside `shared/foundation`.

## 7. Data ownership and database boundary

Every business datum has exactly one owner Cell.

Rules:

- Same-Cell internal JOIN is allowed.
- Cross-Cell source table JOIN is forbidden by default.
- Cross-Cell write is forbidden except through public Command/Application facade.
- Cross-Cell queries must use Query API, Read Model, event projection, materialized view, or query/reporting center.
- L3 should consider independent database schema per Cluster/Cell.
- L4 should consider independent database instance per service.

## 8. Read Model lifecycle

Every Read Model must declare:

- owner;
- source events or source APIs;
- refresh mode;
- max acceptable lag;
- consistency level;
- invalidation strategy;
- allowed usage such as dashboard-only or business-decision-ready.

## 9. Signals

| Signal | Meaning | Naming |
|---|---|---|
| Command | intent to change state | imperative, e.g. `RunAuditCommand` |
| Query | request to read state | e.g. `GetAuditProgressQuery` |
| Event | fact that already happened | past tense, e.g. `AuditCompleted` |
| Metric | health/behavior measurement | e.g. `audit.duration.seconds` |

Do not use events as commands. Do not use logs or metrics as business state.

## 10. Consistency model

- C0: single-Cell consistency.
- C1: same deployment/local transaction consistency.
- C2: cross-Cell eventual consistency through events and Read Models.
- C3: distributed consistency through Saga/TCC/Outbox/Inbox/idempotent consumers.

If strong transaction consistency is required and no distributed transaction capability exists, keep Cells in the same deployment and use local transactions. Do not prematurely split into services.

## 11. Evolution decision matrix

Before splitting a Cell/Cluster into a service, evaluate:

- data consistency;
- performance isolation;
- deployment cadence;
- team ownership;
- failure isolation;
- technology stack needs;
- operational maturity;
- network/latency cost.

If two capabilities need strong local transactions, default to not splitting.

## 12. Fitness functions and rule IDs

Rule IDs are stable references used by tools, PR comments, AI prompts, and reviews.

- `BHA-S-R001`: no cross-Cell direct state mutation.
- `BHA-S-R002`: `shared/foundation` must not import `cells.*`.
- `BHA-S-R003`: no cross-Cell source table JOIN.
- `BHA-S-R004`: formal algorithm experiments require seed/dataset_version/git_commit.
- `BHA-S-R005`: robot control paths require timeout and safety_check.
- `BHA-S-R006`: domain must not depend on infrastructure/HTTP/DB/SDK/ROS runtime.
- `BHA-S-R007`: deprecated code past expiry must be removed or renewed with ADR/issue.

Severity should be configured by project level in `bha.yaml`.

## 13. Evidence layer

Prefer automatically collected evidence:

- git diff changed file count;
- architecture check findings;
- cross-Cell import violations;
- shared pollution warnings;
- expired deprecated items;
- test pass rate;
- build result;
- task recovery rate;
- AI patch failure/repair counts.

If a metric cannot be collected by CI, Git, tests, or telemetry, keep it as review context, not a formal gate.

## 14. Algorithm engineering profile

Add these cells or equivalents:

- dataset_manager;
- data_pipeline;
- experiment_runner;
- algorithm_policy;
- algorithm_kernel;
- evaluator;
- model_registry;
- inference_service;
- monitoring;
- report_generator.

Formal experiments require an `ExperimentConfig` snapshot including seed, dataset version/hash, git commit, config version, environment, model parameters, and metric definitions.

`algorithm_kernel` may depend on PyTorch/JAX/TensorFlow. Do not force framework-free purity onto compute kernels. Keep policy, evaluation rules, data lineage, and deployment governance explicit.

## 15. Robotics engineering profile

Add these cells or equivalents:

- perception;
- localization;
- planning;
- control;
- manipulation;
- safety_guard;
- hardware_adapter;
- simulator;
- telemetry;
- task_executor.

Rules:

- hard real-time control must not depend on remote services;
- safety-critical nodes must have controlled lifecycle or equivalent wrapper;
- BHA-S Command maps to ROS Service/Action;
- Event maps to ROS Topic;
- Query maps to ROS Service/local state;
- Metrics map to diagnostics/telemetry;
- one Cell may contain multiple ROS Nodes;
- define Safety Level S0-S3 and enforce safety gates accordingly.

## 16. AI Coding control loop

AI must not only read rules; it must be controlled by checks.

Loop:

1. read `bha.yaml` and `architecture/cell-map.md`;
2. classify intent and target Cell;
3. edit only relevant files;
4. run tests and `bha_check.py`;
5. repair violations;
6. report remaining debt.

## 17. Vertical slice first

Do not build all architecture layers first. First create one working path from interface to application to domain to infrastructure to observation to test. Widen only after the first slice works.
