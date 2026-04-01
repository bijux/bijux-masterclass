# Capstone

The capstone is an executable plugin runtime for incident-delivery adapters. It is
the course’s integration point for the ideas developed across introspection,
decorators, descriptors, and metaclasses.

## What it demonstrates

- `Field` descriptors that validate and coerce plugin configuration
- an `@action` decorator that preserves signatures and records invocations
- a `PluginMeta` metaclass that gathers fields, generates constructors, and registers plugins
- manifest export driven by introspection rather than action execution
- deterministic, resettable plugin registration suitable for testing

## Run it

From the repository root:

```bash
make COURSE=python-programming/python-meta-programming test
```

From the capstone directory:

```bash
make confirm
```

## Why it matters

Metaprogramming is easiest to misunderstand when each mechanism is taught in
isolation. The capstone forces the mechanisms to coexist:

- descriptors own per-field behavior
- decorators wrap behavior without destroying signatures
- the metaclass owns class-creation invariants and registration
- inspection exposes the system to tooling without triggering side effects
