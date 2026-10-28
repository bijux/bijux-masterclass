# StorageClass contract

A StorageClass is a platform-facing product interface. Its name should communicate a stable service profile rather than expose raw provider parameters.

## Contract fields

Document for every class:

- supported data classes and excluded workloads;
- provisioner and reviewed parameters;
- binding mode and topology;
- reclaim policy;
- filesystem or block mode;
- access modes and driver limitations;
- expansion and mutable-attribute support;
- snapshot, clone, and restore capability;
- encryption and key ownership;
- performance envelope and variability;
- backup integration;
- cost and quota model;
- deprecation and migration path.

## Versioning

Changing provider parameters under an existing class name can alter topology, encryption, durability, cost, or performance for new claims while old claims retain the previous behavior. Treat material changes as a new profile or a governed mutation with compatibility evidence.

## Defaults

A default class is convenient but dangerous for stateful production workloads. Claims that omit `storageClassName` can silently consume whichever class is currently default. Atlas requires explicit classes for authoritative data and uses admission policy to prevent accidental fallback.

## Release oracle

The class is ready only when a real claim has been provisioned, attached, mounted, expanded if promised, snapshotted/restored if promised, and measured under the declared workload shape. Static YAML proves only intent.
