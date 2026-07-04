# Example Cell

## Purpose

Describe the autonomous capability owned by this Cell.

## Owned Data

- `example_*`

## Public Facade

- `application/services/example_service.py`

## Commands

- `CreateExampleCommand`

## Queries

- `GetExampleQuery`

## Events

- `ExampleCreated`

## Metrics

- `example.created.count`
- `example.operation.duration`

## Boundaries

This Cell must not expose domain internals to other Cells. Other Cells must call its public facade, contract, event, or Read Model.
