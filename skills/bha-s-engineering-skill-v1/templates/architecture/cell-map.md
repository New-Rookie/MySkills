# Cell Map

| Cluster | Cell | Purpose | Owned Data | Public Interface | Signals | Owner |
|---|---|---|---|---|---|---|
| default_cluster | example_cell | Example capability boundary | example_* | application facade | ExampleCreated | TBD |

## Rules

- Every core capability belongs to exactly one Cell.
- Every Cell belongs to exactly one Cluster, even during soft-cluster migration.
- Owned Data can only be modified by the owner Cell.
- Cross-Cell collaboration must use public facade, contract, event, or Read Model.
