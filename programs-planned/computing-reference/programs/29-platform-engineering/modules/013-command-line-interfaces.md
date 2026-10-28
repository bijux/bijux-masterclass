---
module_id: PLAT-013
program: Platform Engineering
level: 1
module_number: 13
title: Command-Line Interfaces
status: complete
last_verified: 2026-09-02
---

# Command-Line Interfaces

## One-Page Review

### Governing question

How can a platform team design a command-line interface that is learnable for humans, stable for automation, safe for consequential operations, diagnosable under failure, and semantically consistent with the platform's other interfaces?

### Essential definitions

- A **command-line interface (CLI)** is a versioned contract that maps an invocation context and byte streams to output streams, exit status, durable effects, and recovery information.
- A **command grammar** defines commands, subcommands, options, option arguments, operands, separators, repetition, and constraints.
- An **operand** names the object on which a command acts; an **option** modifies how the action is performed or represented.
- **Human output** is presentation optimized for reading and may adapt to a terminal. **Machine output** is a declared, stable, parseable schema.
- **Standard output** carries the requested result. **Standard error** carries diagnostics, progress, warnings, and prompts when those do not belong to the result.
- An **exit-status contract** maps bounded outcome classes to documented integers; zero means the command satisfied its success contract.
- **Interactive mode** may ask a person for missing decisions when a terminal is attached. **Non-interactive mode** must be deterministic and fail rather than hang for input.
- A **destructive operation** can delete, revoke, overwrite, expose, or make state difficult to recover and therefore requires explicit scope, preview, authorization, and recovery semantics.

### Central model, mechanism, or theorem

Model invocation $I=(G,A,S,E,C,T,L)$ as grammar-selected command $G$, argument vector $A$, standard input $S$, environment $E$, resolved configuration $C$, terminal capabilities $T$, and locale/context $L$. It yields $R=(O,D,X,M,K)$: standard output $O$, diagnostics $D$, exit status $X$, mutations $M$, and continuation evidence $K$. Compatibility requires preserving the documented relation from valid invocation classes to result semantics, not merely keeping an executable with the same name.

### Critical invariants

- The CLI and API expose one capability and operation model; the CLI does not invent hidden platform truth.
- Non-interactive invocations never prompt, open a pager, depend on color, or wait indefinitely for input.
- Machine formats are explicitly requested, versioned, schema-tested, and independent of terminal width, color, locale, and user presentation preferences.
- Requested data goes to stdout; diagnostics go to stderr; secrets go to neither.
- Exit status represents the documented command outcome, including partial and asynchronous results.
- Retries preserve idempotency keys or operation identity; interruption never implies rollback unless the platform proves it.
- Destructive scope is visible before execution and cannot be broadened by an unsafe implicit default.
- Configuration source, precedence, target context, authenticated principal, and effective scope are inspectable without exposing credentials.

### Common failures

Parsing human tables in scripts; printing warnings into JSON; returning zero after partial failure; prompting in CI; using current directory or a mutable default account invisibly; accepting secrets in process arguments; swallowing provider errors; changing field types without a schema version; retrying non-idempotent commands blindly; showing a spinner in redirected output; making `--force` bypass authorization; and confirming deletion with an ambiguous yes/no question that omits exact scope.

### Compact example

`platform service delete payments --environment production --output json --yes` resolves an explicit target, prints a versioned deletion plan, verifies authorization and preconditions, submits an idempotent asynchronous operation, writes one JSON result to stdout, writes warnings to stderr, and exits zero only if submission satisfies the documented contract. It returns an operation ID and command to observe or cancel where supported. Without `--yes`, a terminal may request an exact-name confirmation; a non-terminal fails with a documented interaction-required status and performs no mutation.

### Connections

Retrieve self-service operations from [PLAT-005](005-self-service-and-guardrails.md), provider boundaries from [PLAT-008](008-internal-platforms-and-external-cloud-services.md), team authority from [PLAT-009](009-platform-team-boundaries.md), journey and channel semantics from [PLAT-011](011-developer-journeys.md), and first-deployment evidence from [PLAT-012](012-time-to-first-successful-deployment.md). The next modules compare web portals, APIs, declarative resources, templates, documentation, IDE integration, and cross-channel consistency.

## Governing Question

What must remain stable, explicit, and safe when a person or program invokes a platform capability through a terminal, shell script, CI job, remote runner, or assistive technology?

A CLI is often treated as a convenience wrapper around HTTP calls. That framing misses its public grammar, process environment, streams, exit status, terminal behavior, local configuration, operating-system integration, upgrade path, and scripting ecosystem. Once users build automation around it, whitespace, timing, defaults, and diagnostics can become dependencies.

Good CLI design makes common intent concise while keeping consequential context visible. It offers progressive discovery to a new consumer, deterministic operation to automation, and sufficient evidence to diagnose the same platform operation through another authorized channel.

## Why This Matters

The shell is both a human workspace and a composition runtime. A developer explores commands interactively, then places a successful invocation into a script. A platform team therefore serves two audiences through the same executable: people who benefit from explanation and adaptation, and programs that require stable bytes and outcomes.

POSIX Issue 8 provides current conventions for utility syntax and shell composition, including option/operand distinctions and `--` as an end-of-options delimiter where applicable. GNU coding standards add familiar long options and conventional `--help` and `--version`. These are not universal laws, but deviating without strong reason imposes relearning and parsing risk.

Current Kubernetes guidance tells scripts to request a machine-oriented output form, fully qualify mutable resource versions, and avoid implicit context and preferences. Current Git documentation makes the same boundary concrete: its default long status is human presentation subject to change, while porcelain formats are intended for scripts and insulated from configuration; NUL-delimited output handles pathnames that newline-delimited parsing cannot represent safely.

Security is part of the interface. MITRE CWE-214 records that command arguments and environment entries can be visible to other processes on some operating systems. A convenient `--token secret` option can leak through process listings, shell history, CI logs, telemetry, crash reports, or support transcripts. Secret acquisition needs a deliberately narrower channel and redaction strategy.

Platform operations are frequently asynchronous and consequential. The local process can be interrupted while the remote operation continues. A timeout can mean unknown outcome. A zero exit after “accepted” is not the same as verified completion. The CLI must communicate operation identity, state, evidence, and safe continuation rather than collapse distributed behavior into a spinner.

## Prerequisites and Retrieval

Retrieve capability ownership, consumer segments, cognitive-load analysis, self-service state, provider composition, team boundaries, value hypotheses, developer journeys, and deployment verification from PLAT-001 through PLAT-012. Pay particular attention to durable operation identities, responsibility boundaries, and verified outcomes.

You should understand processes, argument vectors, environment variables, standard input/output/error, exit status, terminals, pipes, redirection, quoting, filenames, signals, configuration, authentication, JSON, API compatibility, asynchronous operations, idempotency, and destructive-action safety.

## Learning Objectives

After completing this module, you should be able to:

1. define a predictable command grammar using commands, options, operands, separators, and consistent vocabulary;
2. separate adaptive human presentation from stable, versioned machine output;
3. allocate results, diagnostics, progress, prompts, and secrets across safe channels;
4. specify exit statuses for success, invalid invocation, denied action, conflict, partial result, and uncertain outcome;
5. design deterministic terminal and non-terminal behavior, including signals, timeouts, and asynchronous continuation;
6. resolve configuration and authenticated context visibly and testably;
7. make destructive and bulk operations previewable, bounded, authorized, and recoverable; and
8. evolve a CLI using compatibility tests, deprecation, telemetry governance, and release discipline.

## Core Exposition

### Start with capabilities and task vocabulary

Derive the CLI from platform capabilities and developer journeys. Use terms consumers already encounter in the API, portal, documentation, events, and support. If the API calls an object an `environment`, the CLI should not call it a `space` unless the distinction is deliberate and documented.

A common grammar is `tool noun verb`, `tool verb noun`, or nested noun-oriented commands. Consistency matters more than ideology. Choose a form that supports discovery, related-command grouping, completion, authorization explanations, and growth without ambiguous parsing. Avoid a flat collection of historical action names.

Keep flags semantically consistent: the same `--environment`, `--output`, `--request-id`, `--timeout`, and `--yes` should mean the same thing everywhere they appear. Do not reuse a familiar flag for a subtly different unit or scope. Require long forms for consequential options in durable examples even when short aliases exist.

### Specify grammar rather than accepting accidental syntax

Document synopsis, commands, options, option arguments, operands, multiplicity, mutual exclusions, defaults, and precedence. Accept `--` before operands that begin with a hyphen. Define whether repeated options append, override, or fail. Reject unknown options and missing arguments with a diagnostic and nonzero status.

Shell quoting happens before the executable sees arguments. Documentation should provide copyable examples that distinguish one argument containing spaces from several arguments, avoid unsafe interpolation, and show standard input or files for complex payloads. The program receives an argument vector, not the original command text.

Treat names and filenames as data. Newlines, leading hyphens, spaces, Unicode, and terminal-control characters can invalidate naive line parsing or produce deceptive display. Machine modes need JSON arrays, length-aware encodings, or documented NUL delimiters rather than whitespace splitting.

### Model invocation and result explicitly

Represent one invocation as

$$
I=(G,A,S,E,C,T,L),
$$

where $G$ is selected grammar production, $A$ arguments and operands, $S$ standard input, $E$ relevant environment, $C$ resolved configuration, $T$ terminal capabilities, and $L$ locale and execution context.

The result is

$$
R=(O,D,X,M,K),
$$

where $O$ is stdout, $D$ diagnostics on stderr, $X$ exit status, $M$ durable mutations, and $K$ continuation evidence such as operation ID, retry token, status locator, or recovery action.

Test the whole relation. A command that returns correct JSON but mutates the wrong account is broken. A command that performs the right mutation but exits nonzero after losing the response has an uncertain outcome, not an ordinary failure. A command that prints a warning before its JSON has broken the machine-output contract.

### Separate human and machine output

Human output may use headings, aligned tables, color, hyperlinks, relative time, pagination, truncation, progress, and suggestions. Detect terminal capabilities conservatively and provide overrides such as `--color=never`, `--no-pager`, and `--quiet`. Accessibility and logging contexts may require plain output even when a terminal exists.

Machine output should be opt-in through a clear flag such as `--output json` and have a published schema. Use stable field names and types, explicit nullability, absolute timestamps with offsets, canonical identifiers, bounded enums, units in names or schemas, and arrays rather than delimiter-packed strings. JSON interoperability follows RFC 8259, but syntactically valid JSON alone does not create a stable semantic contract.

Do not mix modes. Exactly one JSON document or a documented stream of JSON records should appear on stdout. Diagnostics belong on stderr and should themselves support structured form if automation needs them. Human default output should explicitly be non-parseable as a contract.

### Allocate streams and exit statuses

Write the requested result to stdout so it can be piped. Write syntax errors, authorization denials, warnings, progress, and recovery guidance to stderr. `--help` and `--version` are successful requested results and conventionally go to stdout. Never print secrets to either stream.

Define exit classes, for example: zero for the documented success condition; two for invalid invocation; three for interaction required in non-interactive mode; four for authorization or policy denial; five for conflict or failed precondition; six for remote operation failure; seven for partial result; and eight for unknown outcome. Exact numbers are product choices except where a surrounding standard governs them. Stability and documentation matter.

Do not use exit status to encode a resource count. Shells and operating systems constrain its range, and counts do not express outcome semantics. Put data on stdout. When listing across providers partially succeeds, return the successful subset with explicit per-item errors and a partial-result status rather than pretending completeness or discarding useful evidence.

The following synthetic matrix checks core automation and mutation rules. It validates the contract examples, not an implementation or universal exit-code assignment.

<!-- bijux-verify: {"id":"cli-contract-matrix","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"cases=8\npassed=8\nmutations=1\nprompts=0\nsecrets_exposed=0\n","stderr":""}} -->
```python
cases = [
    {"name": "inspect-json", "tty": False, "machine": True, "exit": 0, "mutates": False},
    {"name": "inspect-human", "tty": True, "machine": False, "exit": 0, "mutates": False},
    {"name": "invalid-option", "tty": False, "machine": False, "exit": 2, "mutates": False},
    {"name": "delete-needs-yes", "tty": False, "machine": True, "exit": 3, "mutates": False},
    {"name": "delete-confirmed", "tty": False, "machine": True, "exit": 0, "mutates": True},
    {"name": "denied", "tty": False, "machine": True, "exit": 4, "mutates": False},
    {"name": "conflict", "tty": False, "machine": True, "exit": 5, "mutates": False},
    {"name": "unknown-outcome", "tty": False, "machine": True, "exit": 8, "mutates": False},
]

passed = 0
for case in cases:
    deterministic = case["tty"] or case["exit"] != 3 or not case["mutates"]
    safe_mutation = not case["mutates"] or case["name"] == "delete-confirmed"
    machine_bounded = not case["machine"] or case["exit"] in range(0, 9)
    passed += deterministic and safe_mutation and machine_bounded

print(f"cases={len(cases)}")
print(f"passed={passed}")
print(f"mutations={sum(case['mutates'] for case in cases)}")
print("prompts=0")
print("secrets_exposed=0")
```

### Make interaction a declared mode

Terminal detection is a hint, not consent. A command may run under a pseudo-terminal in automation, and a person may redirect output interactively. Provide explicit `--interactive` and `--non-interactive` controls where behavior differs materially. Environment variables such as `CI` are weaker hints, not authoritative truth.

In non-interactive mode, missing required input fails immediately with the exact field and safe correction. Disable prompts, pagers, editors, browser launch, animation, and unbounded waits. Accept decisions through explicit options or declarative input. Never invent a dangerous default merely to keep a pipeline moving.

Interactive prompts should state action, exact target, environment/account/region, consequence, recoverability, and default. Destructive confirmation should require a strong affirmative action, sometimes re-entering a target name. Confirmation supplements authorization and policy; it does not replace them.

### Resolve configuration and context visibly

Define a precedence order such as command option, standard input or explicit file, environment, project configuration, user configuration, and built-in default. Not every value should be available through every source. Credentials in project files or arguments are unsafe; a context name can be accepted while the credential is obtained from an operating-system store or short-lived identity flow.

Offer a command that explains effective configuration with source provenance and redaction: target endpoint from option, account from project config, region from user config, output from environment, credential from agent. Support an explicit empty value distinct from absent input. Avoid silently reading arbitrary files from the current directory for high-consequence commands.

The XDG Base Directory Specification offers a current convention on relevant Unix-like systems for separating configuration, data, state, cache, and runtime files. Cross-platform tools should use native conventions through a deliberate abstraction and document migration and permission behavior.

### Design authentication and secret input

Prefer short-lived, scoped credentials through an authenticated helper, operating-system credential facility, workload identity, or standard input/descriptor designed for secrets. If environment variables are supported, document their exposure and lifetime; do not assume they are secret. Never accept a secret solely through a command option.

Redact arguments, headers, URLs, environment-derived values, configuration dumps, debug logs, traces, crash reports, and support bundles. Redaction should operate on typed sensitive fields before formatting, not on a fragile string pattern afterward. Do not echo a secret to confirm receipt.

Show authenticated principal, target, expiry, and scopes without revealing credential material. Separate login from authorization: possessing a token does not prove permission for a requested operation. Reauthentication and consent flows must fail safely in non-interactive contexts.

### Treat remote operations as distributed state

For asynchronous operations, return a durable operation identifier, accepted parameters, target, initial state, observation command, and correlation. Offer `--wait` as an explicit client behavior with a documented timeout; it does not change the server operation's identity.

If the local process receives an interrupt, stop local waiting and state whether a cancellation request was sent. Never print “cancelled” when only the client stopped. On network timeout after submission, query by idempotency key or operation ID before retrying. Classify the result as unknown when authoritative state cannot be recovered.

Use idempotency for create, update, and delete intents where feasible. A client-generated request key should survive retries, channel changes, and process restarts. Expose preconditions such as resource version to prevent lost updates. Make retry guidance specific to the operation class rather than always saying “try again.”

### Make destructive and bulk work reviewable

Separate plan from apply. A plan identifies exact resources, derived consequences, policy decisions, dependencies, and unknowns against a named snapshot. Applying should bind to that plan or revalidate and disclose drift. A generic `--force` must not erase authorization, widen selectors, or convert unknown scope into action.

Require explicit environment and selection for bulk destructive commands. Show counts and canonical identifiers, cap accidental fan-out, and support machine-readable plans. Use `--yes` to acknowledge a fully specified plan, not to consent to whatever mutable context later resolves.

Prefer reversible state, retention windows, soft deletion, export, or recovery tokens where the domain permits. State the point of irreversibility. Return per-resource outcomes for partial bulk execution and preserve a continuation mechanism.

### Design help, discovery, and errors together

Every command should offer concise synopsis, purpose, options with defaults and sources, operands, examples, output modes, exit statuses, environment/configuration, consequences, and related commands. Root help explains the model; subcommand help answers the immediate job. Shell completion accelerates known vocabulary but cannot substitute for documentation.

Errors should identify the failed command and object, explain the violated contract in consumer language, preserve provider correlation, state whether mutation occurred, and give safe next actions. Offer more detail through an explicit diagnostic mode without dumping secrets. Link to versioned documentation with a stable error code.

Validate help and examples as interface tests. Completion metadata, docs, generated manual pages, and parser definitions should derive from or check against one command schema so they cannot drift silently.

### Evolve without breaking unseen automation

Treat command names, options, defaults, exit classes, stream allocation, machine schemas, configuration keys, and destructive semantics as compatibility surfaces. Semantic Versioning can communicate changes only after the public contract is declared; a new executable version number does not excuse undocumented breakage.

Additive machine fields may still break strict consumers. Define whether unknown fields must be ignored, allow explicit schema selection, and use contract fixtures across supported versions. Never change a field from string to number in place. Human presentation can evolve more freely when clearly excluded from automation guarantees.

Deprecate with detection, warning on stderr, replacement guidance, machine-readable metadata, and a published removal window. Warnings must not corrupt structured stdout. Keep aliases only when their authority and safety semantics remain identical. Measure command and error classes only with purpose, minimization, aggregation, retention, and opt-out or disclosure appropriate to the context.

## Definitions and Notation

$I=(G,A,S,E,C,T,L)$ is the invocation: grammar production, arguments, stdin, environment, resolved configuration, terminal capabilities, and locale/execution context. $R=(O,D,X,M,K)$ is the result: stdout, stderr diagnostics, exit status, mutations, and continuation evidence.

Let $\Gamma_v$ be the documented CLI contract at version $v$. Compatibility for supported invocation class $i$ requires that the observable semantics of $R_{v+1}(i)$ remain within the guarantees of $\Gamma_v$, unless the consumer explicitly selects a new contract. Byte-for-byte equality is not required for human output; schema and semantic constraints govern machine output.

For bulk targets $B$ and per-target terminal outcomes $o_b$, completeness requires an outcome for every $b\in B$ or an explicit unresolved set $U\subseteq B$. A zero exit status must not imply complete success while $U$ is nonempty unless the documented command success contract explicitly says only submission was requested.

## Mechanisms, Invariants, or Proof Structure

Use a contract-first loop: identify journey and capability; define grammar; classify interactive and automation consumers; specify streams and exit map; define configuration and authentication sources; model operation states; add destructive guardrails; publish machine schemas; generate help and completion; test contract fixtures across terminals and pipes; perform adversarial security review; release; observe bounded product signals; deprecate deliberately.

The semantic invariant keeps CLI, API, portal, and provider state aligned. The stream invariant preserves composition. The non-interaction invariant prevents hidden waits. The context invariant prevents ambient targeting. The identity invariant preserves one remote operation across retries. The safety invariant binds confirmation to explicit scope. The secrecy invariant keeps sensitive values out of visible channels.

Test with TTY and no TTY; stdin open, closed, and redirected; stdout/stderr separate and merged; narrow and wide terminals; color on/off; several locales; filenames with spaces, newlines, leading hyphens, and Unicode; missing configuration; expired identity; denial; conflict; partial provider failure; signal before and after submission; network timeout; duplicate retry; schema downgrade; and old automation fixtures.

## Alternatives and Trade-Offs

**CLI over a shared SDK** centralizes API semantics and authentication. SDK defaults and error types can leak into the user contract; add a CLI-specific compatibility layer.

**CLI as direct HTTP composition** minimizes layers and exposes protocol detail. It duplicates retry, auth, serialization, and evolution logic and can make provider quirks public.

**Human-first default output** improves exploration. It must be explicitly unstable for parsing and paired with machine modes.

**JSON output** is widely interoperable and typed. It is verbose in shells, has number/interoperability constraints, and needs semantic schema versioning.

**Delimited text or NUL records** composes efficiently with Unix tools. Delimiter, escaping, encoding, header, and schema rules must be exact; newline cannot safely delimit arbitrary pathnames.

**Interactive confirmation** prevents some slips. It blocks automation and can become habituated; explicit plan binding and authorization provide stronger controls.

**Config profiles** reduce repetition. They introduce ambient mutable state; explicit target flags and provenance improve reproducibility.

**Bundled plugins** enable domain extension. They expand executable trust, version negotiation, discovery, and support boundaries. A stable contribution API and signed distribution are necessary.

## Failure Modes and Misconceptions

- **“It is just an API wrapper.”** Process, shell, stream, terminal, configuration, and upgrade contracts add distinct responsibilities.
- **“If humans can read it, scripts can parse it.”** Tables, color, localization, truncation, and presentation changes make human output unstable.
- **“Any nonzero status means retry.”** Denial, invalid input, conflict, partial result, and unknown outcome require different actions.
- **“Ctrl-C cancelled the operation.”** It may only stop local observation while remote mutation continues.
- **“`--yes` makes deletion safe.”** It is meaningful only when target, context, plan, authorization, and recovery are already bounded.
- **“Environment variables are secret.”** They may be visible through processes, logs, crash data, or child inheritance.
- **“TTY detection tells us the user.”** Automation can allocate a pseudo-terminal and people can redirect streams.
- **“Adding JSON is enough.”** A parseable document without stable schema and semantics is still an unstable contract.
- **“Aliases are harmless.”** They can retain unsafe defaults and fragment documentation or authorization semantics.
- **“Telemetry tells us developer productivity.”** Command counts describe activity and may expose sensitive work; use bounded product evidence instead.

## Worked Examples

### Example 1

A list command defaults to a colored table with relative ages. Scripts use `--output json --schema v1`; warnings go to stderr. A later column reorder affects humans but not automation, while a schema field-type change requires `v2`.

### Example 2

A service named `-payments` is passed after `--`: `platform service get -- -payments`. The parser treats it as an operand rather than an option. Documentation explains shell quoting for names containing spaces without re-parsing command text.

### Example 3

A CI job omits `--environment`. Instead of reading a developer's mutable default and prompting, non-interactive mode exits three, lists the missing decision on stderr, emits no result, and performs no mutation.

### Example 4

A create request times out after the server accepted it. The CLI queries with the persisted idempotency key. If state remains unavailable, it exits with unknown outcome and prints observation guidance rather than submitting a duplicate.

### Example 5

A bulk inventory spans three providers; one provider fails. JSON stdout contains successful items and a typed error collection, stderr summarizes the failure, and exit seven declares partial result. Consumers do not mistake the subset for a complete inventory.

### Example 6

A login command opens a browser only in explicit interactive mode. Headless mode prints a device-flow locator and reads no hidden prompt. Subsequent `auth status` shows principal, target, scopes, and expiry but never token material.

### Example 7

A database deletion plan names environment, account, resource ID, retained backups, dependents, cost stop, and irreversibility time. `--yes` binds to the plan digest. Drift requires a new plan rather than silently expanding deletion.

### Example 8

A screen reader receives plain progress events on stderr rather than an overwriting spinner. `--no-progress` and `--output json` produce deterministic redirected output. Color never carries the only indication of failure.

### Example 9

A deprecated `--region-name` option maps exactly to `--region`. The warning goes to stderr with removal date and replacement. Contract tests prove JSON stdout and exit semantics remain unchanged during the deprecation window.

### Example 10

A plugin requests unrestricted credential access. Installation and execution fail because its signed manifest lacks the capability. The CLI reports the plugin boundary and does not treat extension code as implicitly trusted platform code.

## Cross-Program Connections

Operating systems define processes, streams, signals, terminals, environment inheritance, permissions, and exit status. Programming languages and parsers implement grammar, typing, Unicode, and error handling. API engineering contributes schemas, compatibility, idempotency, authentication, pagination, and asynchronous operations.

Distributed systems explains timeouts, partial failure, duplicates, uncertain outcomes, and durable correlation. Security engineering covers secret channels, least privilege, injection, untrusted terminal content, plugin trust, and audit. Reliability engineering contributes observation, cancellation, recovery, and diagnostic quality.

Human-computer interaction and accessibility shape progressive disclosure, feedback, prompts, cognitive load, and nonvisual use. Data governance constrains telemetry and configuration. Product management ties the CLI to journeys and outcomes rather than feature parity for its own sake.

## References

- IEEE and The Open Group, [*POSIX.1-2024, Issue 8: Utility Syntax Guidelines and Rationale*](https://pubs.opengroup.org/onlinepubs/9799919799/xrat/V4_xbd_chap01.html), 2024. Current option/operand, delimiter, portability, and future-utility conventions with their rationale.
- GNU Project, [*Standards for Command Line Interfaces*](https://www.gnu.org/prep/standards/html_node/Command_002dLine-Interfaces), current GNU Coding Standards retrieved September 2, 2026. Long-option consistency, POSIX alignment, `--help`, and `--version` conventions.
- Git Project, [*git-status Documentation*](https://git-scm.com/docs/git-status.html), current manual retrieved September 2, 2026. Human output versus stable porcelain formats, configuration independence, versioned records, and NUL delimiters.
- Kubernetes Project, [*kubectl Usage Conventions*](https://kubernetes.io/docs/reference/kubectl/conventions/), current documentation retrieved September 2, 2026. Machine-oriented output, fully qualified resource versions, and avoidance of implicit state in scripts.
- MITRE, [CWE-214: *Invocation of Process Using Visible Sensitive Information*](https://cwe.mitre.org/data/definitions/214.html), CWE 4.20 retrieved September 2, 2026. Exposure of sensitive command arguments and environment values through operating-system process information.
- IETF, [RFC 8259: *The JavaScript Object Notation (JSON) Data Interchange Format*](https://www.rfc-editor.org/rfc/rfc8259), December 2017. JSON grammar, interoperability, encoding, parser, and generator requirements.
- Semantic Versioning, [*Semantic Versioning 2.0.0*](https://semver.org/spec/v2.0.0.html), current specification retrieved September 2, 2026. Version communication relative to a declared public API.
- freedesktop.org, [*XDG Base Directory Specification*](https://specifications.freedesktop.org/basedir-spec/latest/), current specification retrieved September 2, 2026. Separation and precedence of user configuration, data, state, cache, and runtime paths on relevant systems.
- Command Line Interface Guidelines contributors, [*Command Line Interface Guidelines*](https://clig.dev/), retrieved September 2, 2026. Practitioner synthesis on human-first design, streams, interactivity, errors, configuration, signals, and robustness.
- DORA, [*Platform Engineering*](https://dora.dev/capabilities/platform-engineering/), updated January 12, 2026. Current product, critical-journey, clear-feedback, independent-work, and balanced platform-measurement guidance.

## Exercises

### Exercise 1

Design the grammar and contract for `platform environment create`. Specify options, operands, configuration precedence, stdin use, human and machine output, exit statuses, asynchronous operation evidence, and retry behavior.

### Exercise 2

Review a command that prints a progress spinner and warning followed by JSON on stdout, prompts when stdin is redirected, returns zero for partial provider failure, and accepts `--token`. Identify contract violations and propose a compatible migration.

### Exercise 3

Design a safe bulk deletion CLI for expired development environments. Include selection, plan binding, authorization, confirmation, drift, partial failure, interruption, recovery, and audit evidence.

### Exercise 4

Create a contract-test matrix for a list command across terminals, redirection, locale, color, configuration, strange resource names, schema versions, and server failures. State which output may change.

### Exercise 5

Transfer the CLI model to a hospital laboratory-result routing tool. Allocate platform, laboratory, privacy, clinical, and operator authority; design machine output, secret handling, consequential confirmation, and unknown-outcome recovery.

## Answers to the Exercises

### Answer 1

Use `platform environment create NAME --profile PROFILE --project PROJECT --region REGION [--from FILE|-] [--output human|json] [--schema v1] [--wait] [--timeout DURATION] [--request-id ID]`. `NAME` is one operand after options or `--`; repeated singular options fail. Resolve explicit options, explicit input document, approved environment variables, project config, user config, then defaults, while credentials come from an identity helper. Stdin is used only with `--from -`, never as an accidental prompt in non-interactive mode. Human stdout summarizes the target and operation; JSON stdout follows schema v1; diagnostics and progress use stderr. Exit classes distinguish invalid input, interaction requirement, denial, conflict, remote failure, partial result, and unknown outcome. Successful submission returns operation and resource IDs; `--wait` observes the same operation. Retries reuse the persisted request ID and query before resubmitting after uncertainty.

### Answer 2

The spinner corrupts redirected output, the warning makes stdout invalid JSON, the prompt can hang automation, zero misstates completeness, and the token can leak through process lists and history. First add `--output json` with one versioned document on stdout, route diagnostics/progress to stderr, disable animation off-TTY, add `--non-interactive`, introduce a partial-result nonzero status with typed per-provider outcomes, and add a credential helper or protected stdin/file-descriptor flow. Keep old human output temporarily only where compatible. Warn on stderr about `--token`, redact it everywhere, publish a removal window, and detect affected usage through privacy-governed aggregate signals. Contract fixtures prove old supported automation or provide an explicit schema/version migration.

### Answer 3

Selection requires explicit owner, environment class, expiry cutoff, account, and region; it cannot inherit a destructive wildcard. `plan` resolves canonical resource IDs, dependencies, retention, cost, recovery, policy, unknowns, and a snapshot digest. Authorization evaluates each target. Interactive apply displays exact scope and requires a strong confirmation; automation uses `--yes --plan DIGEST`. Apply revalidates the digest and fails on widening drift. It returns a durable bulk-operation ID plus per-resource states; partial completion exits with its documented class. Interrupt stops local waiting and reports whether server cancellation was requested. Soft deletion and recovery tokens are preferred, with the irreversible time stated. Audit evidence records principal, policy, plan, request identity, target outcomes, and correlation without secrets.

### Answer 4

Test human output under wide/narrow TTY, no TTY, color forced/disabled, pager allowed/disabled, and several locales; headings and layout may change within accessibility and meaning guarantees. Test `--output json --schema v1` byte semantics with stdout redirected and stderr separate: field names/types, nullability, enums, timestamps, identifiers, and exactly one document remain stable and locale/color/config independent. Include names with spaces, newline, leading hyphen, Unicode, and control characters; use JSON arrays or NUL records. Test absent and conflicting config with provenance, denied and partial server responses, timeout and unknown outcome, and unknown future fields. Test schema v2 only when explicitly selected. Exit class, stream allocation, mutation, and continuation evidence are stable public behavior.

### Answer 5

The CLI may route an authorized, laboratory-validated result package through a declared technical channel; it cannot create laboratory truth or clinical interpretation. Laboratory authority signs result and correction provenance, privacy authority governs purpose and access, clinical authority governs use and urgent escalation, the platform owns transport state and correlation, and operators execute only authorized procedures. Machine output includes schema version, pseudonymous case correlation, routing state, acknowledgements, correction relation, and typed error without result content unless explicitly authorized. Credentials come from managed identity, never arguments; logs and support bundles redact patient data. Reroute, correction, or cancellation names exact destination and consequence and requires policy plus strong confirmation. Timeout after submission returns unknown outcome with operation ID; the operator queries authoritative state before retrying. Every retry is idempotent, and technical delivery is never reported as clinical receipt or action without the required evidence.
