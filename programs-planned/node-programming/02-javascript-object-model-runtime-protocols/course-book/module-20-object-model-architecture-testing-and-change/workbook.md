# Module 20 Workbook

This workbook is an architecture review. Each answer must name the relevant representation, identity, authority, invariant, and lifecycle. Avoid answers such as “encapsulation is better” without a concrete mechanism.

## A. Runtime-object map

Complete a table for every exported and long-lived ObjectAtlas value:

- live node;
- atlas;
- codec;
- store;
- read view;
- iterator;
- edit session;
- proxy;
- plain record;
- command;
- renderer;
- error.

For each, record identity, owned state, prototype/call behavior, mutating authority, and lifecycle owner.

## B. Invariant-to-operation matrix

Map every public command to the invariants it reads, changes, and re-establishes. Include failure behavior before and after persistence. Identify any operation whose authority is spread across more than one object without an orchestrator.

## C. Representation audit

For node ID, label, kind, attributes, parent, children, aliases, revision, and metadata, state how each appears in:

- live node;
- persistence record;
- custom inspection;
- CLI output;
- traversal view.

Explain every intentional omission or transformation.

## D. Runtime compatibility review

Classify these changes as compatible, conditionally compatible, or breaking:

- method becomes arrow field;
- enumerable property becomes hidden;
- default iterator changes from preorder to breadth-first;
- custom inspection adds a field;
- `Symbol.toPrimitive` begins returning a number for default hint;
- read view changes from live wrapper to frozen snapshot;
- edit session proxy begins accepting nested mutable objects;
- class constructor becomes private and factory remains public.

State which downstream observations are affected.

## E. Test-gap hunt

Given a suite that checks only final JSON output, design the missing tests for:

- descriptors;
- private brands;
- receiver-safe callbacks;
- iteration freshness and early close;
- proxy mutation paths;
- clone identity mapping;
- explicit disposal;
- counterfeit tags;
- persistence reconstruction.

## F. Independent laboratory

Complete [Object Model Audit](../../labs/module-20-object-model-audit/README.md). It is a separate component registry that must survive a cross-layer metadata requirement without exposing mutable internals.

## G. ObjectAtlas completion

Run the full ObjectAtlas contract. Produce:

- one architecture map;
- one invariant register;
- one API surface table;
- one storage schema description;
- one protocol table;
- one lifecycle table;
- one compatibility note;
- passing unit, integration, persistence, and CLI tests.

## H. Independent aliases change

Implement aliases using the chapter specification. Begin with a change-impact map. Do not edit code until every affected layer is listed.

Required evidence:

- parser and validation tests;
- uniqueness and failure-atomicity tests;
- old-file compatibility test;
- canonical persistence test;
- ID/alias lookup test;
- traversal non-impact test;
- clone policy test;
- inspection redaction/bounding test;
- CLI process test;
- release note.

## I. Reconstruction and oral defense

Explain the entire course as one causal chain. For each mechanism, name one ObjectAtlas use and one place where the mechanism was rejected:

- descriptor;
- prototype;
- bound or arrow callback;
- class and private field;
- composition;
- symbol protocol;
- generator;
- proxy;
- weak reference;
- disposal.

Then answer: what is the smallest architecture that still preserves every ObjectAtlas requirement?
