# Evolution Decision Matrix

Use this before splitting a Cell or Cluster into a service.

| Dimension | Keep modular monolith | Consider service split | Score / Notes |
|---|---|---|---|
| Data consistency | Strong local transaction required | Eventual consistency acceptable | |
| Performance isolation | Similar load/resource profile | Very different QPS/GPU/CPU/memory needs | |
| Deployment cadence | Released together | Different release frequency | |
| Team boundary | Same owner/team | Different team ownership | |
| Failure isolation | Failure impact acceptable | Failure must be isolated | |
| Operational maturity | Limited monitoring/CI/CD | Mature CI/CD, tracing, rollback | |
| Network cost | High-frequency low-latency calls | Low-frequency or latency-tolerant calls | |

Decision:

- [ ] keep as Cell
- [ ] move to Cluster
- [ ] split into service
- [ ] revisit later
