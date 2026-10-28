# Verification — API Engineering

## Release conclusion

The revised ten-course source tree passes the complete dependency-light program proof and every course-local core proof. The primary product is the reader-facing course-book corpus. Code, laboratories, capstones, fixtures, and proof routes support the explanations and expose counterexamples; they do not replace the explanations.

The verified program contains one cumulative Analysis Runs Platform story across ten courses, one hundred numbered modules, and nine byte-identical adjacent handoffs. Earlier contract, durability, security, reliability, performance, event, RPC, ownership, graph, and governance guarantees remain visible as the platform matures.

## Learner product

| Course | Title | Course-book pages | Course-book words (program-proof count) |
|---:|---|---:|---:|
| 1 | OpenAPI Contract Engineering | 61 | 57,544 |
| 2 | Contract-Driven API Service Engineering | 61 | 64,487 |
| 3 | API Security Engineering | 61 | 53,611 |
| 4 | API Reliability and Observability Engineering | 61 | 60,223 |
| 5 | API Performance, Capacity, and Traffic Engineering | 61 | 49,018 |
| 6 | Event-Driven API Engineering | 61 | 51,147 |
| 7 | gRPC and Protobuf Engineering | 61 | 52,020 |
| 8 | Distributed API Architecture and Microservices Engineering | 61 | 48,160 |
| 9 | GraphQL Schema and Runtime Engineering | 61 | 46,920 |
| 10 | API Platform, Governance, and Developer Experience Engineering | 61 | 48,980 |

Program-book pages: **13**  
Program-book words: **8,485**  
Total navigated learner pages: **623**  
Total learner-facing words: **540,595**

Every course has:

- eight guide pages;
- a three-page orientation;
- ten self-contained module chapters;
- twelve transfer exercises and twelve matching worked answers per module;
- ten failure-oriented labs with setup, controlled action, oracle, evidence, interpretation, cleanup, and completion gates;
- ten evidence checkpoints;
- a cumulative capstone and explicit incoming/outgoing boundary.

## Program-wide proof executed

```text
PASS ten courses and 100 numbered modules
PASS 610 course-book pages and 13 program-book pages
PASS 623-page exact documentation navigation
PASS 1,200 exercise-to-answer identities
PASS 100 complete laboratory structures
PASS 100 complete checkpoint structures
PASS nine adjacent handoffs — 360 byte comparisons
PASS 571 learner-facing local Markdown targets
PASS chapter depth, answer depth, glossary, repetition, and unfinished-marker guards
PASS Python syntax — 515 files
PASS JavaScript syntax — 75 files
PASS curriculum code fences — Python 95, TypeScript/JavaScript 76
PASS duplicate-key-aware structured data — JSON 895, YAML 407, TOML 18
PASS repository hygiene
```

## Course-local proof executed

1. **OpenAPI Contract Engineering** — OpenAPI 3.1.2 baseline and 3.2.0 frontier parsing, offline references, deterministic bundles, 72 schema fixtures, provider ownership, overlays, Arazzo, and compatibility rejection fixtures.
2. **Contract-Driven API Service Engineering** — 51 Python tests, 28 TypeScript tests, operation and migration parity, idempotency, ETags, cursor behavior, artifacts, webhooks, and compatible-release evidence. Two PostgreSQL tests were explicitly skipped because `TEST_DATABASE_URL` was absent.
3. **API Security Engineering** — threat-to-requirement traceability, operation policy coverage, Python and TypeScript hostile-input/security tests, incident evidence, and accepted/rejected security releases.
4. **API Reliability and Observability Engineering** — Python and TypeScript reliability suites, telemetry structures, SLOs, alerts, runbooks, incident/game-day evidence, and ten rejected reliability mutants. Environment-gated PostgreSQL tests remained explicit skips.
5. **API Performance, Capacity, and Traffic Engineering** — 64 Python and 28 TypeScript tests, benchmark envelopes, HTTP and query-plan mechanisms, admission, caching, traffic controls, capacity models, and ten rejected performance defects.
6. **Event-Driven API Engineering** — AsyncAPI course profile, 41 Python and 22 TypeScript tests, canonical events, delivery, acknowledgement, outbox/inbox, replay, schema evolution, event-time processing, security, dead-letter custody, and release gates.
7. **gRPC and Protobuf Engineering** — 31 Python and 18 TypeScript tests, live local Python gRPC calls, Protobuf presence/wire/compatibility evidence, all four RPC shapes, deadlines, retries, streaming, security, lifecycle, and reversible introduction.
8. **Distributed API Architecture and Microservices Engineering** — 31 Python and 20 TypeScript tests, ownership and dependency proofs, projection and saga mechanisms, delegated capabilities, release choreography, five-process loopback network laboratory, and ten rejected architecture defects.
9. **GraphQL Schema and Runtime Engineering** — 29 Python and 15 TypeScript tests, schema/field ownership, batching, high-water cursors, mutations, authorization-before-I/O, demand control, partial data, subscriptions, release gates, and a loopback composition laboratory.
10. **API Platform, Governance, and Developer Experience Engineering** — 17 Python and 14 TypeScript tests, loopback Platform API, multi-protocol registry, catalog, policy, lifecycle, golden paths, sandbox, SDK/SBOM/provenance profiles, runtime reconciliation, analytics, support, and graduation dossier.

## Inventory supporting the program

```text
Markdown files:       913
Python files:         515
TypeScript files:     321
JavaScript files:     75
JSON documents:       896
YAML documents:       407
TOML documents:       18
```

Counts above describe the source tree before deterministic packaging. Exact release bytes are governed by each course manifest and the root program manifest.

## Evidence boundary

The release environment provided Python, Node.js, TypeScript, GNU Make, and the dependency-light/runtime libraries used by the executed proofs. It did not provide MkDocs, Docker, PostgreSQL command-line tools, Prometheus `promtool`, NATS Server, the AsyncAPI CLI, k6, Locust, Buf, `protoc`, or grpcurl.

Consequently, the program does **not** claim execution of:

- strict MkDocs rendering;
- live PostgreSQL locking, lease takeover, transaction, and mixed-version migration topologies beyond the explicitly available tests;
- Docker or Kubernetes deployment laboratories;
- live Prometheus/collector/Jaeger topologies and native `promtool` validation;
- live NATS JetStream behavior and independent AsyncAPI CLI validation;
- representative k6/Locust capacity evidence;
- independent Buf/`protoc` regeneration and grpcurl reflection;
- operated Backstage, external registries, cloud gateways, hosted identity, or independent signed-provenance infrastructure.

Those routes retain commands, setup, expected oracles, cleanup, and failure criteria. Missing infrastructure is reported as `not-executed`; it is never converted into a pass.

## Packaging requirement

The release packager must verify exact root and course manifests, run the program release proof, build the ZIP twice with byte-identical output, reject duplicate or unsafe paths, verify CRCs and executable modes, extract into a clean directory, rerun all ten course proofs, clean generated artifacts, and verify all manifests again. The machine-readable archive release record is the authority for that final packaging evidence.
