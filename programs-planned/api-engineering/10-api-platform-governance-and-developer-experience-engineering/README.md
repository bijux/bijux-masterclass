# Course 10 — API Platform, Governance, and Developer Experience Engineering

An API platform is not a portal skin, a gateway installation, or a committee that
approves documents. It is an organizational product that makes trustworthy API
work easier to discover, create, publish, consume, evolve, and retire while each
domain team retains ownership of its business facts.

This final course continues the Analysis Runs Platform built through Courses
1–9. The platform already exposes governed HTTP/OpenAPI, event/AsyncAPI,
gRPC/Protobuf, and GraphQL interfaces. Course 10 turns those independently
engineered interfaces into **Analysis API Platform 1.0**: a catalog, immutable
contract registry, policy engine, lifecycle service, scorecard system, golden
path, documentation portal, sandbox, SDK publication pipeline, runtime inventory,
consumer-support model, and federated governance process.

## What the learner builds

The cumulative capstone proves that a platform can:

- discover every component, API, owner, consumer, and runtime dependency;
- publish immutable multi-protocol contract releases by digest;
- apply policy as code without replacing engineering judgment;
- distinguish pass, review-required, exception, and rejection outcomes;
- govern proposal, experiment, active use, deprecation, and retirement;
- generate a safe API project from a maintained golden path;
- publish task-oriented documentation, examples, and isolated sandboxes;
- release Python and TypeScript SDK artifacts with SBOM and provenance evidence;
- synchronize runtime routes without moving domain authorization into a gateway;
- measure time-to-first-success, adoption, support burden, and deprecated usage;
- operate through a federated model in which the platform team enables and domain
  owners remain accountable.

## Reader-first structure

[`course-book/`](course-book/index.md) is the authoritative product. Every
numbered module contains one complete chapter, twelve transfer exercises,
matching worked answers, one controlled laboratory, and one evidence checkpoint.
The capstone and proof routes make the book's claims executable; they do not
replace the teaching.

Choose one primary implementation track in Courses 2–10. Use the other track to
compare semantics and execute shared-vector parity. Platform guarantees must
match across languages; internal syntax and framework structure need not be
artificially identical.

## Course sequence

1. Platform product model and operating boundaries
2. Catalog, ownership graph, and metadata authority
3. Contract registry and multi-protocol publication
4. Governance as code, evidence, scorecards, and exceptions
5. Lifecycle, compatibility, deprecation, and retirement
6. Golden paths, templates, and self-service provisioning
7. Documentation, discovery, sandboxes, and onboarding
8. SDKs, CLIs, artifacts, SBOMs, and provenance
9. Runtime control plane, usage intelligence, and support
10. Federated governance, platform operations, and final defense

## Start

```bash
make help
make doctor
make predecessor-proof
make capstone-tour
make core-proof
make manifest-proof
```

Then begin with [`course-book/start-here.md`](course-book/start-here.md).
