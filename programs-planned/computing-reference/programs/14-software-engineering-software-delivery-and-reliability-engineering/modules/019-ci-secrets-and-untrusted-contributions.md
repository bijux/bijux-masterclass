---
module_id: SDRE-019
program: Software Engineering: Software Delivery & Reliability Engineering
level: 1
module_number: 19
title: CI Secrets and Untrusted Contributions
status: complete
last_verified: 2026-09-06
---

# CI Secrets and Untrusted Contributions

## One-Page Review

### Governing question

How can continuous integration evaluate contributor-controlled code without allowing that code, its metadata, its dependencies, or its artifacts to exercise repository, signing, deployment, or infrastructure authority?

### Essential definitions

- an **untrusted contribution** is any revision or input not yet authorized to exercise the target system's privileges;
- a **secret** is confidential data such as a token, key, or password, while a **capability** is any authority to act, including ambient runner access that is not represented by a secret string;
- a **trust boundary** separates executions with different authority or assumptions;
- a **principal** is an identity to which policy grants authority;
- **least privilege** gives a principal only the capabilities, scope, and lifetime needed for one operation;
- a **privileged trigger** starts a job with authority unavailable to ordinary untrusted validation;
- **credential federation** exchanges an authenticated workload identity for a short-lived credential instead of storing a long-lived credential in CI;
- an **identity claim** states an authenticated property such as issuer, audience, subject, repository, revision, workflow, or environment;
- **artifact poisoning** makes a privileged consumer accept attacker-controlled output as trusted input;
- a **persistent runner** retains machine state across jobs; an **ephemeral runner** is created or cleaned for a bounded execution;
- **redaction** suppresses recognized values in logs; it does not prevent a process from reading or exfiltrating those values;
- an **immutable reference** identifies dependency content rather than a movable name;
- **promotion** is the controlled transition of a revision or artifact into a more privileged delivery stage.

### Central model, mechanism, or theorem

Let $C(j)$ be the set of capabilities available to job $j$, and let $S$ be the set of sensitive capabilities. For every job $u$ that executes untrusted-controlled code, the primary separation invariant is

$$
C(u) \cap S = \varnothing.
$$

The invariant covers more than injected secret values: repository write tokens, cloud metadata, signing services, shared caches, persistent runner residue, privileged sockets, internal networks, and writable artifact channels are capabilities too. A later privileged job may act only from a trusted workflow and after independently binding its subject, policy, and artifact digest to the reviewed revision.

### Critical invariants

- classify trust from executable influence, not merely fork versus internal branch;
- run untrusted code without sensitive credentials, write tokens, signing authority, deployment access, or reusable privileged state;
- never check out or evaluate an untrusted revision in a privileged trigger context;
- treat titles, branch names, commit messages, paths, configuration, dependency manifests, and archives as untrusted data;
- do not interpolate untrusted data into generated shell or expression syntax;
- default token permissions to none or read-only and grant narrowly per job;
- prefer short-lived federated credentials whose claims bind repository, workflow, environment, and ref;
- isolate untrusted jobs on clean ephemeral runners without host control sockets or privileged internal reachability;
- cross a trust boundary only through validated, digest-bound, provenance-aware artifacts;
- separate build/test from publication, signing, deployment, commenting, and label mutation;
- pin external automation by immutable content identity and review transitive code;
- preserve authorization, token issuance, artifact, approval, and promotion audit evidence.

### Common failures

Common failures include exposing a long-lived deployment key to tests, checking out a pull-request head under a privileged event, treating internal branches as trusted, injecting a pull-request title into a shell script, relying on masking to stop exfiltration, running untrusted jobs on persistent self-hosted hosts, mounting a container engine socket, sharing writable caches across trust domains, accepting an artifact by filename alone, using broad wildcard OIDC subjects, approving once and then running changed code, trusting movable action tags, and letting a validation job publish or deploy.

### Compact example

A fork changes a `Makefile`. An unprivileged job may check out that revision and test it on a disposable runner with no secrets and read-only repository access. It emits an artifact plus digest. A separate trusted workflow, defined on the protected base revision, verifies the approved revision, artifact digest, provenance, and policy before obtaining a five-minute publishing token. The first job cannot publish; the second never executes the fork's `Makefile`.

### Connections

[SDRE-016](016-merge-queues.md) binds admission evidence to an exact candidate, [SDRE-017](017-quality-gates.md) defines policy decisions, and [SDRE-018](018-handling-flaky-ci.md) preserves uncertain evidence. [SDRE-020](../ROADMAP.md) next optimizes feedback time without concealing risk.

## Governing Question

CI exists to execute candidate-controlled programs. That is its value and its danger. A contributor can alter source code, tests, build scripts, package hooks, dependency locks, configuration, filenames, generated data, or a compiler plugin. If the same execution receives a release key or repository write token, then review has already lost: malicious code can use the authority before the proposed change is accepted.

The governing problem is therefore authorization, not secret storage alone. We must decide which code can influence an execution, what capabilities that execution receives, what data may cross into a privileged stage, and what independent evidence binds a later privileged action to the intended revision.

## Why This Matters

Build logic is executable production infrastructure. A one-line dependency lifecycle hook can read environment variables, a test can query a cloud metadata endpoint, and a crafted title can become shell syntax if a workflow generates scripts by interpolation. Confidentiality is only one concern: a job may alter a release, poison a cache, sign an artifact, write to a registry, reach an internal database, or persist on a runner without ever printing a secret.

GitHub's current security reference warns that privileged `pull_request_target` and `workflow_run` contexts become vulnerable when they check out untrusted pull-request content; the same guidance recommends immutable full-length commit references for third-party actions [1]. Its compromised-runner reference explicitly states that log redaction is not a true security boundary and describes direct and transformed exfiltration [2]. GitLab's current merge-request pipeline documentation similarly warns that fork code may try to steal parent-project secrets and restricts protected variables and runners to specified protected, same-project conditions [3]. These are platform examples of a general rule: code that can execute can use every capability reachable from its process and environment.

Current practice increasingly replaces stored cloud keys with federated workload identity. GitHub's OIDC reference requires cloud trust conditions and documents audience and subject claims for scoping token issuance [4]. Federation reduces credential lifetime and storage, but a permissive subject rule can still authorize an attacker-controlled workflow. Identity must be bound to the trusted workflow and delivery context, not merely to an organization name.

## Prerequisites and Retrieval

Retrieve process, environment variable, file descriptor, network route, virtual machine, container, cache, artifact, digest, digital signature, principal, authentication, authorization, confidentiality, integrity, least privilege, default deny, input validation, shell quoting, dependency, revision, branch, protected environment, audit log, and incident response.

From SDRE-002 through SDRE-005 retrieve artifact identity, reproducibility, provenance, and supply-chain controls. From SDRE-011 through SDRE-018 retrieve CI triggers, workflows, dependencies, candidate identity, parallel isolation, merge queues, gates, and uncertain outcomes. Security Engineering owns threat modeling, credential systems, cryptography, and adversary depth; Platform Engineering owns runner fleet enforcement. This module owns how delivery workflows compose those controls around untrusted contributions.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish secrets from the broader set of capabilities exposed to a CI job;
2. identify every contributor-controlled input that may influence execution;
3. derive and apply the untrusted-job capability-separation invariant;
4. distinguish unprivileged validation from privileged promotion;
5. explain event-context hazards without relying on one platform's names;
6. prevent command, expression, cache, artifact, and runner-state injection;
7. design least-privilege job tokens and federated workload identities;
8. bind privileged actions to reviewed revisions and verified artifact digests;
9. test authorization failures and preserve audit evidence;
10. respond to suspected credential or runner compromise without hiding uncertainty.

## Core Exposition

**Start with executable influence.** A contribution is untrusted when its author or contents have not been authorized for the capabilities under consideration. A pull request from a fork is an obvious example, but an internal branch is not automatically trusted. A compromised developer account, generated dependency update, vendored tool, or changed workflow file can introduce attacker-controlled execution.

Inventory all inputs that may become code. Source and tests are only the beginning. Build definitions, package installation hooks, compiler plugins, linters, test collectors, documentation generators, configuration templates, container build instructions, dependency metadata, fixture archives, and checked-in binaries can execute or influence executable selection. Repository metadata—titles, bodies, labels, branch names, email fields, and commit messages—can become code when interpolated into a script or query.

Trust is capability-relative. A revision might be sufficiently reviewed to receive permission to comment on its own pull request but not to sign a release. Model explicit trust classes and transitions rather than a universal `trusted=true` flag.

**Model authority as capabilities.** A secret string grants authority only when a service accepts it. Conversely, authority can exist without a named secret. A runner might have an instance role, a client certificate on disk, an authenticated container daemon socket, a writable package cache later consumed by release jobs, a service account mounted by an orchestrator, or network access to an unauthenticated internal service.

For each job, inventory process environment, files, token permissions, host devices, sockets, network routes, identity endpoints, API access, caches, artifacts, logs, approval interfaces, and future jobs influenced by its output. Ask what a malicious command could do immediately and what persistent influence it could leave.

Confidentiality controls do not substitute for authorization. Encryption at rest protects stored credentials from some disclosure paths. Masking reduces accidental log exposure. Neither stops an executing process from making an authenticated request, splitting a value across messages, encoding it, or sending it over an allowed network path.

**Separate validation from privilege.** An untrusted validation job checks out and executes the candidate under minimal authority. It can compile, lint, test, and report through a platform-controlled result channel. It should not publish, sign, deploy, mutate repository state, approve changes, or write to caches later trusted by privileged jobs.

A privileged job runs from trusted workflow logic after policy has authorized the subject. It may comment, label, publish, sign, or deploy, but each operation deserves its own principal and scope. It does not execute contributor-controlled code merely because a human clicked approve. A useful design divides the process into:

1. untrusted execution producing evidence in an isolated domain;
2. immutable recording of revision and artifact identities;
3. independent policy evaluation in trusted code;
4. explicit authorization of one privileged operation;
5. short-lived credential issuance;
6. promotion with auditable subject and output.

The stages can be implemented as separate workflows, services, queues, or hosts. The security property comes from capability separation and verified handoff, not from visual job boundaries in one configuration file.

**Understand trigger context.** CI event names encode different trust assumptions. A normal pull-request event commonly runs candidate code with reduced authority. A base-context event may deliberately grant base-repository tokens and secrets so trusted automation can label or comment. Combining the latter authority with checkout and execution of the candidate head crosses the boundary in the wrong direction.

Do not memorize one unsafe keyword and assume all other triggers are safe. Trace: which workflow revision defines the job, which source revision is checked out, which actor caused the event, which token permissions are computed, which secrets are available, and which caches or environments are shared. Reruns and chained workflows need the same analysis. A trusted downstream workflow that downloads and executes arbitrary output from an untrusted upstream job is still executing untrusted influence.

**Treat data as data.** Workflow engines often expand expressions before invoking a shell. If a pull-request title is inserted directly into generated shell text, shell metacharacters become syntax. Pass untrusted values through a typed action input or environment variable, quote them for the receiving language, validate permitted form, and avoid `eval` or secondary parsing.

Quoting is language- and context-specific. Shell quoting does not make a value safe as JSON, SQL, a regular expression, a path, or a command option. Prefer APIs that separate structure from data. When invoking a process, use an argument vector rather than constructing a shell command. Treat leading hyphens, newlines, Unicode normalization, path separators, archive entries, symbolic links, and enormous inputs as adversarial cases.

**Minimize job tokens.** Begin with no permissions, then add the smallest read permission or single write operation needed by each job. Do not give the entire workflow broad permissions because one final job publishes. Separate principals for repository status, package publication, provenance signing, and deployment so compromise of one does not imply all.

Scope credentials by resource, action, environment, and time. Prefer a token that can upload one package version for minutes over a long-lived token that can delete an entire registry namespace. Ensure failure, cancellation, and rerun paths do not accidentally reuse authority beyond the intended attempt.

Protected environments and required reviewers add a policy gate before selected authority becomes available. They are not code sanitizers. If the privileged job runs the untrusted revision after approval, the approved malicious instruction still executes. Approval must bind an immutable subject, and any subsequent code change invalidates it.

**Use federation carefully.** With workload identity federation, a CI job obtains a signed identity token from the automation platform and exchanges it with a cloud or secret service. The recipient validates issuer, signature, audience, subject, expiry, and other claims before issuing a short-lived capability. No long-lived cloud key need be stored in the repository's CI secret store.

Federation changes the credential path; it does not remove authorization design. A trust rule such as “any repository in this organization” may let an attacker create or compromise a weak repository and request the production role. Bind claims to immutable repository identity where available, trusted reusable workflow, protected environment, permitted ref, and intended audience. Grant token-minting permission only to the precise privileged job.

Check expiration and reject tokens outside a narrow clock-skew allowance. Do not trust an unverified claim merely because it appears in a JSON payload. The receiving service must validate the signed token and its semantics.

**Isolate runners.** An untrusted job can alter every writable part of its runner and may exploit the kernel, container runtime, or privileged devices. Containers on one host are not necessarily a trust boundary, especially when they share host mounts or a daemon socket. Route untrusted work to clean, bounded, minimally networked execution environments.

Ephemeral means more than deregistering an agent. Provision or restore a known image, avoid reusable credentials, constrain metadata services, restrict egress where practical, limit internal network routes, remove host control sockets, bound CPU, memory, storage, and time, then destroy or securely reset the environment. Preserve runner logs outside the destroyed host. GitHub's current runner reference recommends ephemeral self-hosted runners for autoscaling and notes that a clean environment limits exposure from previous jobs [5].

Persistent self-hosted runners can retain processes, modified tools, credentials, files, or poisoned caches. If they must handle trusted work, prevent untrusted revisions from reaching them. If untrusted work requires specialized hardware, use dedicated isolation, attestation, reset, and scheduling policy appropriate to the threat.

**Partition caches.** A cache is both data and a future influence channel. An untrusted job that writes compiler objects, package archives, generated scripts, or executable tool caches can affect a later privileged build. Separate cache namespaces and write authority by trust domain. Prefer content-addressed, verified dependencies and rebuild across privilege boundaries.

A cache key containing a trusted branch name is insufficient if fallback lookup lets a privileged job restore an untrusted entry. Document read and write paths, lookup prefixes, eviction, and integrity checks. Never use cache hit as proof of provenance.

**Validate artifact handoff.** An artifact uploaded by an untrusted job remains untrusted. A digest proves bytes are unchanged relative to a recorded value; it does not prove the bytes are safe or came from an authorized builder. Bind artifact digest to revision, workflow identity, inputs, builder, and policy evidence. Validate archive paths, file types, sizes, symbolic links, nested archives, manifests, and expected outputs before privileged consumption.

Prefer promote-over-rebuild only when the initial builder is trusted for the release claim. If the initial build ran untrusted code in a lower-trust environment, its output may be useful evidence but unsuitable as a release binary. A trusted builder can rebuild the reviewed revision hermetically and compare reproducibility where appropriate.

Do not execute artifact-supplied scripts during verification. Parse data with bounded libraries, extract into a new directory without path traversal, and treat filenames as untrusted. A privileged workflow that sources an uploaded environment file has simply converted artifact data into code.

**Control automation dependencies.** An action, plugin, container image, installer, or reusable workflow runs with the job's authority. A movable tag can later resolve to different code. Pin external automation to an immutable full content identity, verify its origin, review updates, and constrain its permissions and network access. Pinning does not prove benevolence; it makes the reviewed identity stable.

Transitive installers deserve the same analysis. A trusted top-level action that downloads an unsigned “latest” binary at runtime is not fully pinned. Record resolved dependency and image digests in evidence where feasible.

**Design safe reporting.** An untrusted job still needs to report results. Prefer the CI platform's own job conclusion, artifact upload channel with no read-back privilege, or a narrow broker that validates schemas and writes one status. Do not hand the job a general repository token merely to post a comment.

Sanitize displayed output against active content, terminal escapes, formula injection, and misleading links. Preserve diagnostic value while excluding credentials and sensitive infrastructure details. Limits on size and count prevent logs and artifacts from becoming denial-of-service channels.

**Test negative authorization.** A secure workflow should prove denials as well as success. Use controlled fixtures that attempt repository writes, cloud token requests from disallowed subjects, access to metadata endpoints, traversal archives, cache writes across trust domains, command injection through metadata, and use of expired or wrong-audience identity tokens. Tests run in a safe non-production environment with canary credentials and explicit egress controls.

Validate configuration statically, but also exercise platform event semantics because computed permissions and secret availability can depend on repository settings. Re-evaluate after changing trigger, runner group, permission default, environment, cache policy, reusable workflow, or identity-provider trust rule.

**Audit and respond.** Record event, actor, workflow and revision, checked-out subject, runner identity and image, effective permissions, secret identifiers—not secret values—identity claims, token issuance, artifact and provenance digests, approvals, policy version, privileged requests, and final outputs. Protect audit evidence from the job it observes.

If compromise is suspected, stop privileged workflows, revoke and rotate affected credentials, invalidate sessions and signing authority as applicable, quarantine runners and artifacts, preserve evidence, identify every reachable capability, and inspect downstream mutations. Secret rotation alone is insufficient if an attacker changed workflows, packages, releases, deployment state, caches, or trust policies. Restore from known-good configuration and re-establish artifact identity before resuming.

## Definitions and Notation

Let $J$ be the set of CI jobs and $C(j)$ the capabilities reachable by job $j$. Let $U \subseteq J$ be jobs influenced by untrusted executable content and $S$ the sensitive capabilities: write, publish, sign, deploy, mint credentials, reach protected services, or persist influence into privileged execution.

The isolation objective is

$$
\forall u \in U,\quad C(u) \cap S = \varnothing.
$$

This is a design invariant, not proof that the implementation has no vulnerability. The inventory must include direct and indirect capabilities.

Represent a promotion request as

$$
r=(q,w,e,d,p,a,t),
$$

where $q$ is immutable source revision, $w$ trusted workflow identity, $e$ protected environment, $d$ artifact digest, $p$ policy version, $a$ approving authority, and $t$ attempt identity. Authorization evaluates the complete tuple; changing any bound field requires a new decision.

For a federated identity token $x$, let $iss(x)$, $aud(x)$, $sub(x)$, $iat(x)$, and $exp(x)$ be issuer, audience, subject, issued-at time, and expiry. At evaluation time $T$, a simplified acceptance predicate is

$$
Valid(x,T)=Sig(x) \land iss(x)=I \land aud(x)=A \land sub(x)\in P \land iat(x)-\delta \le T < exp(x)+\delta,
$$

where $I$ is the configured issuer, $A$ intended audience, $P$ the explicitly permitted subject set, and $\delta$ a bounded clock-skew allowance. Real provider policy also constrains role, resource, workflow, repository, environment, and requested operation.

## Mechanisms, Invariants, or Proof Structure

**Capability-separation argument.** Suppose untrusted job $u$ can execute arbitrary contributor instructions. If sensitive capability $s$ belongs to $C(u)$, then those instructions may invoke $s$; hiding its representation does not change reachability. Removing every sensitive capability makes direct invocation through the modeled interfaces impossible. This argument depends on a complete inventory and sound isolation, so implementation testing remains necessary.

**Noninterference requirement.** Untrusted values may affect validation results, but they must not select privileged command structure, credential scope, identity-provider trust policy, or the subject of promotion. A privileged decision can consume an untrusted claim only after independent parsing, validation, and binding to trusted evidence.

**Approval binding.** Approval of tuple $r$ authorizes that tuple, not a mutable branch name. If revision $q$ or digest $d$ changes, equality fails and the prior approval cannot authorize the new subject. This prevents “approve, then push different code” from preserving privilege.

**Artifact-integrity distinction.** If $H(b)=d$ for artifact bytes $b$, digest verification establishes equality to the recorded bytes under the hash assumptions. It establishes neither safety nor builder trust. Provenance and authorization evidence are separate predicates.

**Executable policy model.** The following model evaluates five representative job designs. It models declared capabilities and bindings, not operating-system isolation or a real CI platform.

<!-- bijux-verify: {"id":"ci-trust-policy-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"fork_test=allowed\nprivileged_head_checkout=denied:untrusted-code-with-sensitive-capability\nshort_lived_release=allowed\nunpinned_action=denied:mutable-automation-dependency\npersistent_runner=denied:reusable-runner-state\nsecret_masking_prevents_exfiltration=False\nartifact_digest_binding=True\n","stderr":""}} -->
```python
sensitive = {"repository-write", "publish", "sign", "deploy", "oidc-mint"}

def evaluate(job):
    reasons = []
    if job["untrusted_code"] and set(job["capabilities"]) & sensitive:
        reasons.append("untrusted-code-with-sensitive-capability")
    if job["untrusted_code"] and job["persistent_runner"]:
        reasons.append("reusable-runner-state")
    if not job["automation_pinned"]:
        reasons.append("mutable-automation-dependency")
    if job["federated"] and not job["claims_bound"]:
        reasons.append("unbound-federated-identity")
    return "allowed" if not reasons else "denied:" + ",".join(reasons)

jobs = {
    "fork_test": {
        "untrusted_code": True, "capabilities": ["repository-read"],
        "persistent_runner": False, "automation_pinned": True,
        "federated": False, "claims_bound": False,
    },
    "privileged_head_checkout": {
        "untrusted_code": True, "capabilities": ["repository-write"],
        "persistent_runner": False, "automation_pinned": True,
        "federated": False, "claims_bound": False,
    },
    "short_lived_release": {
        "untrusted_code": False, "capabilities": ["publish", "oidc-mint"],
        "persistent_runner": False, "automation_pinned": True,
        "federated": True, "claims_bound": True,
    },
    "unpinned_action": {
        "untrusted_code": False, "capabilities": ["repository-read"],
        "persistent_runner": False, "automation_pinned": False,
        "federated": False, "claims_bound": False,
    },
    "persistent_runner": {
        "untrusted_code": True, "capabilities": ["repository-read"],
        "persistent_runner": True, "automation_pinned": True,
        "federated": False, "claims_bound": False,
    },
}

for name in jobs:
    print(f"{name}={evaluate(jobs[name])}")
print("secret_masking_prevents_exfiltration=False")
approved = {"revision": "abc123", "digest": "sha256:789", "workflow": "release"}
observed = {"revision": "abc123", "digest": "sha256:789", "workflow": "release"}
print(f"artifact_digest_binding={approved == observed}")
```

## Alternatives and Trade-Offs

**One workflow versus separated workflows.** One workflow is simpler to read but makes authority inheritance and output channels easy to confuse. Separate workflows or services clarify trust boundaries, but chained triggers and artifacts must still be authenticated and validated.

**Long-lived secret versus federation.** A stored secret works with many services and offline tools but creates rotation and theft exposure. Federation removes stored cloud keys and narrows lifetime, while adding identity-provider availability and claim-policy complexity.

**Persistent versus ephemeral runner.** Persistent runners reduce startup cost and preserve large caches, but retain attacker influence. Ephemeral runners improve isolation at provisioning, cleanup, logging, and capacity cost.

**Open network versus restricted egress.** Open egress supports arbitrary dependencies and debugging but enables exfiltration. Allowlisted mirrors and proxies reduce paths while requiring dependency governance and exception handling.

**Promote artifact versus trusted rebuild.** Promoting exact bytes avoids rebuild drift. A trusted rebuild avoids releasing output from an untrusted builder but can lose byte identity. Choose according to builder trust, reproducibility, and provenance requirements.

**Shared versus partitioned cache.** Sharing maximizes hit rate but creates poisoning and confidentiality paths. Partitioning by trust domain costs storage and misses but preserves authority separation.

**Automatic versus human privilege gate.** Automated policy is consistent and fast. Human review can judge unusual risk but is vulnerable to fatigue and does not neutralize code. Both must bind the immutable subject.

**Rich contributor reporting versus narrow broker.** Direct API tokens permit flexible comments and labels but expand authority. Platform results or a schema-validating broker expose less capability at the cost of formatting freedom.

## Failure Modes and Misconceptions

- **“No secret variable means no privilege.”** Instance roles, sockets, networks, files, caches, and write channels may grant authority.
- **“Private repositories contain trusted code.”** Account compromise and unreviewed branches still exist.
- **“Only source files are untrusted.”** Build scripts, dependencies, tests, data, archives, and metadata can execute or steer execution.
- **“A container isolates the job.”** Host mounts, daemon sockets, kernel sharing, and network reachability can cross the boundary.
- **“Masked secrets cannot leak.”** Redaction targets recognized log representations, not arbitrary use or exfiltration.
- **“Approval makes code safe.”** Approval authorizes a bound subject; it does not rewrite malicious instructions.
- **“A privileged trigger is safe if the workflow file comes from the base.”** It becomes unsafe when base-defined logic executes the untrusted head or its scripts.
- **“Fork protection solves internal contributions.”** Trust must follow executable influence and authority, not repository topology.
- **“Read-only token means harmless.”** private source, issue data, artifacts, internal networks, and future cache influence can still be sensitive.
- **“Short-lived token means least privilege.”** A brief token may still be broad enough to destroy or publish critical resources.
- **“OIDC removes secrets.”** It removes some stored credentials; token-minting authority and trust rules remain sensitive.
- **“Checking issuer is enough.”** audience, subject, expiry, signature, workflow, and resource constraints matter.
- **“Digest means safe artifact.”** It proves byte identity to a recorded digest, not provenance or safety.
- **“A filename identifies an artifact.”** Names are mutable and collision-prone; bind content and subject identities.
- **“Caches are only performance data.”** restored executables and generated state can control privileged behavior.
- **“Immutable pin means trustworthy code.”** it stabilizes identity but does not establish quality or intent.
- **“One approved run covers later pushes.”** changed revision or digest invalidates the authorization.
- **“Rotating a leaked key finishes response.”** persistent runner state, releases, workflows, packages, and trust policy may also be compromised.

## Worked Examples

### Example 1

**Situation.** A fork changes application code and the `Makefile`; tests need no private service. **Reasoning.** Run the fork revision on a disposable runner with no sensitive capabilities and read-only source access. Upload bounded test results through the platform channel. Do not grant a comment or write token to the test process. **Conclusion.** Untrusted validation is useful precisely because it is capability-separated.

### Example 2

**Situation.** A workflow triggered in the base repository checks out the pull-request head and receives a repository write token. **Reasoning.** The head controls build scripts, so arbitrary untrusted instructions share a job with sensitive capability. Therefore $C(u)\cap S\ne\varnothing$. Move code execution to an unprivileged event and let trusted automation consume only validated results. **Conclusion.** Trusted workflow definition does not make checked-out untrusted code safe.

### Example 3

**Situation.** A pull-request title is `good"; publish --all; #` and is inserted directly into a shell condition. **Reasoning.** Expression expansion constructs new shell syntax before execution. Pass the title as an environment value or typed action input, quote it, validate length and form, and never evaluate it. **Conclusion.** Repository metadata is untrusted data and must not shape command syntax.

### Example 4

**Situation.** A job receives a masked registry password. The log shows `***`, so the team claims it cannot leak. **Reasoning.** Malicious code can use the password directly, transform it, split it across output, or send it over the network. Redaction only reduces accidental display. Remove the credential from untrusted execution and restrict egress. **Conclusion.** Masking is hygiene, not an authorization boundary.

### Example 5

**Situation.** Untrusted tests run in a container with `/var/run/docker.sock` mounted. **Reasoning.** The socket can control sibling containers and commonly the host-level container runtime, allowing mounts or inspection beyond the job. Remove the socket and use a dedicated nested or remote builder with explicit policy. **Conclusion.** A host control interface defeats the intended container boundary.

### Example 6

**Situation.** A release job restores any cache whose key starts with `linux-build-`; fork jobs can write matching entries. **Reasoning.** An attacker stores a modified compiler object or executable tool, and fallback lookup imports it into the privileged job. Partition cache namespaces and write authority by trust domain; rebuild privileged outputs from verified inputs. **Conclusion.** Cache lookup is a cross-job influence channel.

### Example 7

**Situation.** An untrusted job uploads `release.zip`; a privileged job extracts and signs it. **Reasoning.** Filename and digest equality only identify submitted bytes. Validate provenance and approved revision, reject traversal and symlink entries, bound sizes, avoid executing supplied scripts, and decide whether the builder was trusted for release. Otherwise rebuild in a trusted environment. **Conclusion.** Artifact handoff needs authorization and safe parsing, not merely download success.

### Example 8

**Situation.** Cloud trust accepts any OIDC subject beginning with the organization's name. **Reasoning.** A weaker repository or workflow may satisfy that wildcard and request the production role. Restrict issuer and audience, immutable repository identity, trusted workflow, protected environment, permitted ref, role, resource, and short lifetime. **Conclusion.** Federation is secure only as its claim policy.

### Example 9

**Situation.** A maintainer approves a deployment workflow, then the contributor pushes a new commit before it runs. **Reasoning.** Compare current tuple $(q,w,e,d,p,a,t)$ with the approved tuple. Revision and likely digest differ, so authorization fails and new review is required. **Conclusion.** Approval attaches to immutable subject identity, not a moving branch.

### Example 10

**Situation.** A persistent runner handled a malicious test and later signs a legitimate release. **Reasoning.** The first job may leave a process, replace a tool, alter a cache, or capture future material. Stop scheduling, quarantine the host and its outputs, revoke reachable credentials, inspect mutations, restore from a known image, and reissue evidence. **Conclusion.** Runner compromise survives secret rotation unless persistence and downstream effects are addressed.

## Cross-Program Connections

- Security Engineering owns adversary models, credential lifecycle, cryptographic validation, isolation assurance, and incident response depth.
- Platform Engineering owns runner groups, ephemeral provisioning, network segmentation, secret brokers, cache services, and policy enforcement.
- Software Architecture owns trust boundaries, brokers, dependency direction, and separation of privileged responsibilities.
- Testing & Quality Engineering owns adversarial authorization tests, negative cases, and evidence adequacy.
- Operating Systems owns processes, namespaces, files, credentials, devices, and kernel isolation mechanisms.
- Network Engineering owns egress controls, internal reachability, proxies, metadata paths, and segmentation.
- API & Service Engineering owns scoped service tokens, audience semantics, idempotent privileged operations, and audit APIs.
- Cloud Engineering owns workload identity federation, cloud roles, protected environments, and resource-level policy.

## References

1. GitHub, [Secure use reference](https://docs.github.com/en/actions/reference/security/secure-use), official GitHub Actions documentation, current guidance on untrusted inputs, privileged triggers, least privilege, and immutable action references. Retrieved 2026-09-06.
2. GitHub, [Compromised runners](https://docs.github.com/en/actions/concepts/security/compromised-runners), official GitHub Actions documentation, current capability and exfiltration analysis. Retrieved 2026-09-06.
3. GitLab, [Merge request pipelines](https://docs.gitlab.com/ci/pipelines/merge_request_pipelines/), official documentation, current fork, protected-variable, and protected-runner rules. Retrieved 2026-09-06.
4. GitHub, [OpenID Connect reference](https://docs.github.com/en/actions/reference/security/oidc), official documentation, issuer, audience, subject, and trust-condition semantics. Retrieved 2026-09-06.
5. GitHub, [Self-hosted runners reference](https://docs.github.com/en/actions/reference/runners/self-hosted-runners), official documentation, current ephemeral-runner behavior and operational cautions. Retrieved 2026-09-06.
6. OpenID Foundation, [OpenID Connect Core 1.0 incorporating errata set 2](https://openid.net/specs/openid-connect-core-1_0.html), final specification, 2023, identity-token validation foundations.
7. National Institute of Standards and Technology, [Secure Software Development Framework (SSDF), SP 800-218](https://csrc.nist.gov/pubs/sp/800/218/final), Version 1.1, 2022, secure build and software-development practices.
8. SLSA, [Build: Requirements for producing artifacts](https://slsa.dev/spec/v1.2/build-requirements), Specification v1.2, current approved build-platform, provenance, isolation, and external-parameter requirements. Retrieved 2026-09-06.

## Exercises

### Exercise 1

Define untrusted contribution, secret, capability, trust boundary, privileged trigger, federation, artifact poisoning, and promotion. Explain why “no secrets” is weaker than “no sensitive capabilities.”

### Exercise 2

Given an untrusted job with capabilities `{source-read, cache-write, docker-socket}` and sensitive set `{cache-write, repository-write, docker-socket, sign}`, compute their intersection. Trace two attack paths and propose a capability-minimal replacement.

### Exercise 3

A privileged base-context workflow checks out a fork, runs its dependency installer, writes a status, and uploads a package using one broad token. Diagnose every boundary failure and redesign the flow without losing fork validation.

### Exercise 4

Design a workload-identity trust policy for publishing one package from a protected environment. Specify issuer, audience, subject, workflow, revision or ref, environment, role scope, token lifetime, approval binding, and denial tests.

### Exercise 5

A research team must test external contributions on a rare accelerator available only through persistent self-hosted machines. Design a defensible system that balances useful testing with runner persistence, proprietary data, internal-network reachability, caches, reporting, and later trusted workloads.

## Answers to the Exercises

### Answer 1

An untrusted contribution is a revision or input not authorized for the target capability. A secret is confidential credential data; a capability is any reachable authority to read, write, publish, sign, deploy, mint, communicate, or persist influence. A trust boundary separates executions with different authority or assumptions. A privileged trigger supplies authority not present in ordinary validation. Federation exchanges authenticated workload identity for a short-lived credential. Artifact poisoning causes a more privileged consumer to accept attacker-controlled output. Promotion is the governed transition into a more privileged delivery stage. “No secrets” ignores ambient roles, sockets, networks, writable caches, files, and service channels; “no sensitive capabilities” addresses reachable action rather than credential representation.

### Answer 2

The intersection is `{cache-write, docker-socket}`. Through `cache-write`, attacker code can store an executable or object restored by a later privileged build. Through `docker-socket`, it may control containers, inspect sibling state, or mount host resources. Replace the job with source-read access plus a narrow platform-controlled result upload on a clean ephemeral runner. Give it a trust-partitioned read-only dependency cache or verified mirror, no shared privileged cache writes, no host daemon socket, restricted internal routes, bounded egress, and resource limits. A separate trusted job may populate trusted caches from verified inputs.

### Answer 3

The privileged trigger and fork checkout combine sensitive authority with untrusted executable influence. The dependency installer executes fork-controlled hooks. One broad token violates least privilege by coupling status and publication; package upload occurs before trusted authorization. Redesign as an unprivileged fork workflow with no secrets, read-only repository access, disposable runner, pinned automation, and bounded test-result upload. A trusted base workflow reads a schema-validated conclusion to post status through a narrow broker. After merge or exact-revision approval, a protected release workflow defined from trusted code rebuilds or verifies the bound artifact, obtains a short-lived package-scoped credential, and publishes. No privileged stage executes fork scripts.

### Answer 4

Accept only tokens signed by the configured CI issuer for the package registry's exact audience. Match immutable repository identity, the reviewed release workflow identity, protected `production-release` environment, and protected release ref or an explicitly bound revision. The role may create one package version in one namespace but cannot delete versions or administer the registry. Issue it for minutes and only after an approval whose tuple includes revision, workflow, environment, artifact digest, policy version, and attempt. Denial tests cover wrong issuer, signature, audience, repository, workflow, environment, ref, revision, expired and not-yet-valid times, excessive role, changed artifact, rerun after code change, and token request from an untrusted validation job. Provider-side logs must bind issuance to claims and publication.

### Answer 5

Create a dedicated runner pool and trust domain used only for external contributions; never schedule later release or sensitive internal work on those machines. Remove proprietary datasets and long-lived credentials, block metadata endpoints and internal routes, constrain egress through audited mirrors, and expose the accelerator through the narrowest device interface. Restore a measured base image before each job, use per-job accounts and namespaces, bound time and storage, monitor for residual processes, and quarantine the machine after anomalous behavior. Partition or disable writable caches; verify dependencies by digest. Return results through a schema-limited broker rather than a general token. If hardware cannot be reliably reset or isolated, run only sanitized simulations for external changes and require a trusted maintainer to reproduce accelerator tests after review. Evaluation should credit explicit residual risk, isolation evidence, reset verification, and the rule that these runners never become a bridge to privileged workloads.
