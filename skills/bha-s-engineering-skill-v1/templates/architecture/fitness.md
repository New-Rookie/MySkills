# Architecture Fitness Functions

| Rule ID | Name | Severity | Automated? | Tool | Notes |
|---|---|---|---|---|---|
| BHA-S-R001 | No cross-Cell direct state mutation | error | partial | bha_check | |
| BHA-S-R002 | Shared foundation cannot import cells | error | yes | bha_check | |
| BHA-S-R003 | No cross-Cell source table JOIN | warning | partial | bha_check | |
| BHA-S-R004 | Formal experiments require reproducibility fields | error | partial | bha_check | |
| BHA-S-R005 | Robot control paths require timeout and safety_check | warning | partial | bha_check | |
| BHA-S-R006 | Domain must not depend on infrastructure/runtime SDKs | error | partial | bha_check | |
| BHA-S-R007 | Expired deprecated code must be removed | warning | partial | bha_check | |
