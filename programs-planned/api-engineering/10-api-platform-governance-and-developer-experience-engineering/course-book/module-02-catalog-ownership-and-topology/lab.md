# Lab 02 — Build and reconcile the ownership graph

## Setup

Run `make catalog-proof`. Inspect `capstone/catalog/entities.json` and
`catalog-info.yaml`.

## Controlled action

Create four scratch defects: an unknown owner, an API with no provider, a
component consuming an unknown API, and two records with the same canonical
identity. Also create one observed runtime component not present in the source
catalog.

## Oracle

The first four defects fail catalog validation. The runtime-only component is
reported as an unregistered observation, not silently adopted as an authoritative
entity.

## Required evidence

Produce `reports/module-02-catalog-reconciliation.json` containing rejected
records, source authority, derived relations, freshness, and reconciliation
recommendations.

## Cleanup

Remove scratch entities and rerun catalog proof.

## Completion gate

You can answer who owns, implements, consumes, and supports every active API
without relying on a free-text search.
