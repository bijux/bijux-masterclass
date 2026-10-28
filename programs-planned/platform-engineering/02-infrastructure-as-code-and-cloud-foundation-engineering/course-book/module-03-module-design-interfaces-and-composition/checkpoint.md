# Checkpoint — Module Interfaces and Evolution

## Required evidence

Retain:

- module responsibility statement and owned-object list;
- decisions explicitly left to the root;
- typed input contract with rejected invalid combinations;
- bounded output contract and caller inventory;
- provider/alias requirement evidence;
- flat composition diagram;
- compatibility classification for the next module version;
- moved-address upgrade proof;
- one rejected escape-hatch input;
- one justified decision not to create a module.

## Decision defense

Explain which decisions the caller owns and which the module intentionally withholds. Show how semantic keys preserve identity and why a child provider block would obscure target authority. Defend the output surface as an API rather than a dump of provider internals.

## Progression gate

You pass only when the abstraction eliminates unsafe states, has a migration path, and can evolve without accidental replacement. More directories or wrappers do not count as modularity.
