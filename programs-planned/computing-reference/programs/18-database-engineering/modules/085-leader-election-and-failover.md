---
module_id: DBE-085
program: Database Engineering
level: 2
module_number: 85
title: Leader Election and Failover
status: complete
last_verified: 2026-09-05
---

# Leader Election and Failover

## One-Page Review

### Governing question

How can a replicated database replace an unavailable writer without electing an unsafe copy, creating two writers, losing more acknowledged history than its contract permits, or returning a divergent former leader to service?

### Essential definitions

A **failure detector** produces suspicions from incomplete observations; it does not prove that a remote node is dead. **Eligibility** determines whether a replica's history, durable/applied frontier, integrity, version, resources, and failure-domain state permit promotion. **Election** chooses at most one authority for a term/epoch under a membership rule. **Fencing** prevents nodes with older authority from mutating protected state or serving as the current writer. **Promotion** changes an eligible replica from recovery/follower mode to authoritative write mode and records a new history. A **term**, **epoch**, or **view** is a monotonically ordered authority generation. A **witness** participates in authority decisions without necessarily holding full data. **Switchover** is planned role transfer; **failover** responds to unplanned loss or isolation. **Failback** is a new controlled role change, not reversal of time. **Rejoin** brings an old node into the current history through rewind, catch-up, or reseed.

### Central model, mechanism, or theorem

Safety requires a conjunction:

$$
Promote(c,e) \Rightarrow Eligible(c,F_{required},H) \land Won(c,e,M) \land Fenced(<e) \land DurableEpoch(c,e).
$$

`Eligible` protects data/history; `Won` protects unique authority under membership M; `Fenced` excludes stale terms at every write boundary; `DurableEpoch` makes the decision survive restart. A heartbeat timeout supplies none of these by itself. A new leader must cover the required acknowledged frontier or the control plane must explicitly declare/reconcile loss. Election quorum, replication acknowledgement quorum, and read quorum can be different sets with different proofs.

### Critical invariants

- At most one unfenced writer epoch can mutate the protected database authority.
- A vote/lease/lock is bound to authenticated member identity, durable term, membership epoch, and database history.
- Each voter grants at most the protocol-allowed vote in a term and persists it before replying when the proof requires durability.
- The elected candidate passes history ancestry, required frontier, integrity, compatibility, resource, and role checks.
- Fencing reaches storage, network, credentials, service discovery, and downstream side effects—not only a process flag.
- Client routing changes only after promotion/fence evidence is committed and health/readiness pass.
- Ambiguous client transactions are reconciled by stable identity across the history change.
- An old leader never rejoins as writer; divergent state is preserved for audit, then rewound or reseeded.
- Recovery of redundancy is a separate completion criterion after service restoration.

### Common failures

Failures include equating missed heartbeats with death; promoting the most responsive but stale replica; using two-node mutual timeouts without a witness/quorum; storing election terms only in memory; letting both partitions reach an uncoordinated witness; changing membership while counting old and new majorities incorrectly; fencing only client traffic while the old writer retains storage/jobs/replication credentials; announcing the endpoint before recovery finishes; retrying ambiguous writes without idempotency; using a numeric LSN from a divergent timeline; immediately “failing back” to the recovered old leader; and declaring the incident over while the cluster remains one failure from outage.

### Compact example

The last acknowledged required frontier is 995 on history H7. Candidate r1 is intact at durable/apply 1,000 on H7; r2 is at 990; r3 reports 1,010 on sibling history H6. Only r1 is eligible. A majority election in membership epoch 12 grants r1 term 8, durably records it, and obtains a storage/network fence token 8. Requests bearing old term 7 are rejected. r2 can catch up; r3 must be reconciled/rewound or reseeded. Highest bare position would have chosen the wrong history.

### Connections

Retrieve [Failure Models](071-failure-models.md), [Physical Replication](081-physical-replication.md), [Synchronous and Asynchronous Replication](083-synchronous-and-asynchronous-replication.md), and [Replication Lag and Stale Reads](084-replication-lag-and-stale-reads.md). Continue through [the program roadmap](../ROADMAP.md) to sharding, distributed transactions, consensus-backed replication, global transactions, and consistency/latency/availability evaluation.

## Governing Question

When clients cannot reach a database writer, the writer may be crashed, paused, overloaded, partitioned, isolated from the observers, or healthy on the other side of a control-plane failure. Starting another writer can restore service or create split brain. The difference is not the quality of the timeout; it is whether authority, data eligibility, and fencing form a complete protocol.

Leader election answers who may lead. Failover additionally chooses a safe candidate, completes recovery, excludes former authority, publishes a new write endpoint, resolves uncertain transactions, and rebuilds redundancy. Each stage has distinct evidence and rollback rules.

## Why This Matters

A false failover can be worse than downtime. Two primaries can accept conflicting keys, allocate overlapping sequences, execute jobs twice, acknowledge transactions into divergent histories, and send irreversible external effects. A stale promotion can discard transactions that synchronous policy claimed durable. A correct promotion with incomplete routing can send clients to both terms.

Automation is essential because humans respond slowly and inconsistently under pressure, but automation increases blast radius when its assumptions are wrong. A production design must make unsafe states unrepresentable or fail closed: no eligible candidate means no automatic promotion; no fence means no write publication.

Current PostgreSQL 18 documentation provides promotion and timeline mechanisms but explicitly states that PostgreSQL does not supply the system software that detects primary failure and notifies the standby; it emphasizes informing/fencing the old primary to avoid both systems acting primary. Current MySQL 8.4 supports GTID-based positioning and asynchronous connection source switching, but connection failover and database-writer election are different responsibilities. These product boundaries were checked on 2026-09-05.

## Prerequisites and Retrieval

Retrieve these ideas:

- an unavailable response does not distinguish crash from delay or network partition;
- replication frontiers are comparable only within compatible histories/epochs;
- acknowledgement policy determines the frontier successful writes are expected to have reached;
- receive, durable flush, apply, visibility, and promotion readiness are separate;
- consensus/election safety depends on durable terms/votes and intersecting membership decisions;
- leases require carefully bounded clocks and delayed-message assumptions;
- fencing tokens must be checked by the resource being protected;
- recovery replays one chosen history and promotion normally creates a new branch/term;
- service discovery, connection pools, DNS, proxies, credentials, background jobs, and CDC consumers cache authority;
- client timeouts around failover create unknown transaction outcomes requiring stable IDs/status lookup.

This module develops the control workflow around replicated database state. DBE-088 later gives consensus-backed replication its full treatment; here consensus results are used only where an election/authority mechanism claims them.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish failure detection, eligibility, election, fencing, promotion, routing, and rejoin;
2. derive candidate requirements from acknowledged durability and history ancestry;
3. explain why two-node heartbeat failover cannot safely distinguish failure from partition;
4. evaluate majority, witness, lease, external-lock, and manual election designs;
5. design term/epoch and fencing-token enforcement across every write surface;
6. sequence planned switchover and unplanned failover with explicit cut points;
7. reconcile ambiguous transactions and divergent former primaries;
8. validate failover through deterministic partition, crash, storage, clock, and control-plane tests.

## Core Exposition

**Start with the failure model.** List process crash, host loss, storage failure, network partition, asymmetric reachability, pause, overload, clock error, region loss, control-plane loss, credential failure, operator action, corruption, and Byzantine behavior if relevant. Most database failover systems assume crash faults plus bounded operational behavior, not malicious nodes. Do not claim Byzantine safety from TLS or a majority count.

Specify recovery objectives and priorities. Is it safer to stop writes than risk split brain? Which acknowledged transactions may be lost? How long can failover take? Must reads remain available? What human authorization is required for uncertain data or fencing? Different transaction classes may have different acknowledged frontiers, but promotion chooses one actual history.

**Treat detection as suspicion.** Heartbeats, TCP health, query probes, process managers, storage signals, and cloud APIs provide observations. A timeout means “no qualifying response before this observer's deadline.” Network delay, GC/pause, CPU starvation, DNS, credentials, and the observer itself can cause it.

Use multiple signals to reduce needless transitions, but no finite collection makes an asynchronous timeout a proof of death. Safety comes from election and fencing. Tune detection for recovery time versus false suspicion; use monotonic time locally; record observer identity, sequence, evidence, and uncertainty. Avoid synchronized retries and simultaneous candidacy with randomized/backed-off timers where the protocol supports it.

**Separate eligibility from election.** Build a candidate record containing database/system ID, history/timeline ancestry, durable and applied frontiers, latest complete transaction, checksum/integrity state, recovery status, software/schema/config compatibility, encryption keys, storage health/capacity, replication role, intentional delay, failure domain, and last trusted observation.

Derive $F_{required}$ from the strongest relevant acknowledged commit contract. A candidate below it is ineligible for a “no acknowledged loss” promotion. If no candidate covers it, either remain unavailable or invoke an explicitly authorized data-loss procedure that inventories missing transaction IDs and changes the claim. Equal or higher offsets on sibling histories do not qualify.

**Choose an authority mechanism.** Common designs include:

- a replicated consensus group elects a leader by term and up-to-date log rules;
- an external strongly consistent coordinator grants an epoch/fencing token;
- a witness breaks ties for a primary/standby pair;
- a time-bounded lease grants authority under clock/delay assumptions;
- a human performs manual election after verified fencing.

The coordinator itself needs a failure model and operational lifecycle. A single witness can become a single availability point or be reachable from both data partitions unless it grants one durable term. A distributed lock is useful only if linearizable enough for the claim and every protected resource rejects expired/older tokens.

**Persist terms and votes.** A node must not forget on restart that it voted or observed a higher term. Otherwise it can grant conflicting authority. Bind decisions to membership epoch M and database history H. Authenticate members and reject replayed messages from old epochs.

Membership change is part of safety, not inventory editing. Joint/overlapping configurations ensure that old and new decision quorums intersect during transition. Removing failed nodes merely to obtain a smaller majority can create two live majorities if the old configuration continues elsewhere.

**Fence before publication.** Process termination is one fence, but the old leader may restart or remain alive across a partition. Stronger fencing can revoke storage access, power off a host, detach disks, invalidate credentials, change a storage generation, or require a monotonically increasing token on every write.

Fence all mutation channels: database client writes, replication source role, scheduled jobs, migration workers, message consumers, sequence/ID allocators, backups that alter state, DDL automation, and external side effects. A proxy fence alone fails if clients use cached direct endpoints. A flag in the old database fails if the new partition cannot write it.

The protected resource must enforce the fence. If storage accepts writes without checking epoch, handing the application token 8 is ceremonial. Prefer fencing that is independently observable and idempotent. If fence outcome is unknown, fail closed or escalate rather than assume success.

**Promote as a transaction-like workflow.** A safe unplanned sequence is:

1. declare an incident/mode epoch and stop or drain new write admission where possible;
2. gather detector evidence and current membership;
3. establish exclusive authority through election/lock/lease;
4. fence older terms and verify enforcement;
5. select an eligible candidate covering required history or authorize quantified loss;
6. fetch/replay all available chosen-history log and complete recovery;
7. durably create the new database term/timeline and write token;
8. enable write services/jobs only under the new token;
9. publish routing with readiness and token validation;
10. reconcile ambiguous transactions and rebuild replicas/retention.

Some protocols interleave election, log selection, and commitment more tightly. Preserve their proof rather than mechanically reordering steps. The invariant is that no writable publication occurs without both exclusive authority and safe recovered state.

**Design planned switchover separately.** Reject or drain new writes, wait for in-flight transactions, establish a final source frontier, require the target to durably receive/apply it, disable and fence the old writer, transfer authority in a new epoch, promote, publish, and verify. Because the old source is cooperative, uncertainty is lower, but skipping fencing still risks restart or stale routing.

Rollback before authority transfer can resume the old leader after validating no new term. After the new leader accepts a write, “rollback” is another switchover or recovery operation; simply restarting the old leader creates divergence.

**Handle client-visible ambiguity.** Connections break during failover. A transaction may be absent, prepared, committed only on the old history, committed and replicated, or committed with a lost response. Stable command/transaction IDs allow lookup across logs and the new leader. Clients should retry by identity, not issue a semantically new operation.

Inventory transactions between the chosen candidate frontier and the old source endpoint. For synchronous promises, absence indicates protocol/operation failure. For asynchronous promises, it can be expected loss exposure but still needs business reconciliation. External effects may need an outbox/inbox or compensating workflow.

**Publish and cache authority safely.** Proxies/service discovery should carry cluster ID and leader epoch. Backends reject writes with stale tokens even if routing is wrong. Drain or reset connection pools because existing sessions can outlive DNS/endpoint updates. Prevent replicas in recovery/read-only mode from passing write readiness.

Read routing must also validate history. A stale old primary can return internally consistent but divergent reads. Session tokens from the old history need ancestry/reconciliation as DBE-084 described.

**Rejoin the former leader.** Preserve disks/logs for forensic and transaction reconciliation. Verify it cannot serve traffic. Compare timelines/terms and locate the common ancestor. If supported and evidence is intact, rewind divergent blocks/history to the new leader, then replay forward. Otherwise reseed from a verified base. Never copy “newer-looking” files or merge physical histories manually.

Current PostgreSQL `pg_rewind` is designed to synchronize a diverged cluster with the current source using timeline history and WAL around the divergence; it still requires subsequent WAL replay. That does not make every old primary safely rewindable—required WAL, checksums/full-page evidence, credentials, and configuration must satisfy documented prerequisites.

**Restore redundancy and normal guarantees.** Immediately after promotion the system may be in a degenerate state with one copy, weaker acknowledgement, no remote failover, and high retained-log pressure. Track a second objective: re-establish replicas across required failure domains, current backups/archives, monitoring, synchronous membership, read capacity, and tested failover readiness.

Do not close the incident at endpoint recovery. Record the actual recovery time, lost/ambiguous transactions, maximum unavailable interval, fence evidence, new term, rebuilt members, weakened durability interval, and gaps between design and observation.

**Test the complete path.** Rehearse process/host/storage/zone failures; symmetric and asymmetric partitions; pauses; slow disks; full logs; corrupted candidate; stale/high numeric positions on sibling history; witness/coordinator loss; delayed/duplicate votes; term persistence loss; clock steps for leases; fence failure; cached routes; client response loss; background jobs; old leader restart; and rejoin.

For every execution, assert one writable epoch, required frontier coverage, durable election state, enforced fences, valid new history, correct routing, bounded/known ambiguous transaction set, and restored redundancy. Test the automation itself under repeated failover so an old command cannot promote a second candidate later.

The finite executable model below separates eligibility, election term, and fencing. It selects r1 because only r1 covers the required frontier on the accepted history, then demonstrates rejection of a term-7 write after term 8. It is not a network, storage, consensus, failure-detector, database recovery, or fencing implementation.

<!-- bijux-verify: {"id":"finite-failover-eligibility","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"required_frontier=995\neligible=r1\nelected=r1\nnew_term=8\nfence_token=8\nold_term_write_accepted=false\nnew_term_write_accepted=true\nr2_reason=below_required_frontier\nr3_reason=wrong_history\nevidence=finite_failover_eligibility\n","stderr":""}} -->
```python
required_frontier = 995
accepted_history = "H7"
members = [
    {"id": "r1", "history": "H7", "durable": 1000, "intact": True},
    {"id": "r2", "history": "H7", "durable": 990, "intact": True},
    {"id": "r3", "history": "H6", "durable": 1010, "intact": True},
]

eligible = [member for member in members
            if member["history"] == accepted_history
            and member["durable"] >= required_frontier
            and member["intact"]]
assert len(eligible) == 1
elected = eligible[0]
new_term = 8
fence_token = new_term

def storage_accepts(write_term):
    return write_term >= fence_token

print(f"required_frontier={required_frontier}")
print(f"eligible={elected['id']}")
print(f"elected={elected['id']}")
print(f"new_term={new_term}")
print(f"fence_token={fence_token}")
print(f"old_term_write_accepted={str(storage_accepts(7)).lower()}")
print(f"new_term_write_accepted={str(storage_accepts(8)).lower()}")
print("r2_reason=below_required_frontier")
print("r3_reason=wrong_history")
print("evidence=finite_failover_eligibility")
```

## Definitions and Notation

- $c$: candidate replica.
- $e$: proposed monotonically increasing leader term/epoch/view.
- $M$: durable membership configuration/epoch governing the decision.
- $H$: accepted database history and ancestry.
- $F_{required}$: minimum history frontier required by acknowledged-write policy or explicit recovery decision.
- $Eligible(c,F,H)$: predicate over history/frontier, integrity, compatibility, recovery, resources, and role.
- $Won(c,e,M)$: election/authority predicate defined by the protocol for membership M and term e.
- $Fenced(<e)$: protected resources reject mutation authority from every older term.
- $DurableEpoch(c,e)$: term/leader decision survives required crashes and restart.
- **Split brain:** multiple unfenced authorities accept conflicting mutation histories.
- **Witness:** voting/authority participant that may not contain a full database copy.
- **Degenerate state:** service restored with less redundancy or weaker failure tolerance than normal.
- **Rewind:** reconstruct a former member from the common ancestor and current chosen history.

## Mechanisms, Invariants, or Proof Structure

**Uniqueness argument.** In majority-based elections over one fixed membership, any two majorities intersect. If each voter grants at most one durable vote per term, two different candidates cannot both obtain a majority in the same term. This premise fails with forgotten votes, inconsistent membership, unauthenticated duplicate identities, or a protocol that permits multiple grants.

**Freshness/eligibility argument.** Election uniqueness alone can choose one stale leader. Requiring candidate history to contain the protected committed/acknowledged prefix prevents a leader from discarding that prefix under the protocol's assumptions. Bare offsets are insufficient when histories diverge; ancestry and transaction identity participate.

**Fencing argument.** Even after a unique election, an old leader may not learn the result. If every mutation boundary accepts only the greatest durable epoch token and token e has been installed, requests from terms below e are rejected. If any write path ignores the token, the conclusion does not cover that path.

**Failure-detection limit.** A silent node and a partitioned node produce the same missing-response observation to an isolated observer. Timeout policy can suspect and initiate an election, but cannot safely authorize a second writer without an intersecting authority decision and effective fence.

**Switchover cut.** Once old write admission is closed at final frontier F and the target proves compatible durable/applied coverage through F, transferring authority/fence to the target preserves the chosen history. Any untracked write after F or publication before fencing violates the cut.

## Alternatives and Trade-Offs

| Design | Advantage | Cost or risk | Required evidence |
| --- | --- | --- | --- |
| Manual failover | human judgment for ambiguity | slow, error-prone, inconsistent | checklist, dual control, drills |
| Automated timeout + consensus | fast and safe under protocol assumptions | quorum/control-plane dependency | term/vote/membership tests |
| External linearizable lock | separates coordination from data nodes | coordinator dependency and fencing integration | token enforcement at resources |
| Two data nodes + witness | economical tie-breaking | witness placement and durable-vote risk | partition matrix and identity tests |
| Lease leadership | efficient steady state | clock/delay assumptions and expiry gaps | bounded-clock/message evidence |
| Storage/power fencing | strong exclusion | provider latency/blast radius | verified idempotent fence result |
| Proxy-only fencing | easy routing change | bypass/cached connections remain | never sufficient alone for writes |
| Most-up-to-date candidate | minimizes loss/catch-up | needs compatible history and integrity | transaction/history comparison |
| Planned switchover | controlled final frontier | write drain and coordination | cutover/reversal tests |
| Rewind old leader | faster than full reseed | needs common ancestor and required log | vendor prerequisites and validation |
| Full reseed | clean chosen history | transfer time and reduced redundancy | base/log manifest and restore test |

## Failure Modes and Misconceptions

- **“Heartbeat failure proves the primary died.”** It proves only missing timely observation.
- **“Election makes the candidate safe.”** Election chooses authority; eligibility protects history and data.
- **“The highest LSN is newest.”** Positions on sibling histories are not scalar-comparable authority.
- **“A majority of connections is a quorum.”** Identities, durable votes, and one membership epoch matter.
- **“A witness cannot cause data loss because it stores no data.”** Its vote can authorize a stale data candidate if eligibility is not coupled.
- **“Read-only mode fences the old primary.”** Privileged sessions, restart, direct storage, jobs, or configuration can bypass it.
- **“Changing DNS completes failover.”** Cached sessions/endpoints and direct clients remain; the database must reject stale terms.
- **“Promotion can happen before recovery finishes.”** Publishing writes before chosen-history recovery creates an unsafe state.
- **“Timeout means the client transaction aborted.”** Commit may have occurred before connection loss.
- **“Failback returns to the old normal.”** After new writes, it is a new switchover or a destructive divergence decision.
- **“The old leader can catch up from both branches.”** Physical histories do not merge by copying newer files.
- **“Service restored means resilience restored.”** A single surviving primary is still degenerate.
- **“Consensus handles every external effect.”** Jobs, queues, caches, object stores, and payments need their own token/idempotency boundaries.
- **“More automation always reduces downtime.”** Unsafe or flapping automation can multiply promotions and damage.

## Worked Examples

### Example 1

**Situation.** Primary p and standby r stop hearing each other, but both can serve local clients. Each has a five-second heartbeat timeout.

**Reasoning.** Observations are symmetric with a crash from each side. If r self-promotes and p remains writable, split brain results. A durable quorum/witness must grant one new epoch and protected resources must fence the other. If neither can obtain authority, write unavailability is the safe result.

**Conclusion.** Two-node mutual timeout cannot safely choose a writer during partition by itself.

### Example 2

**Situation.** Required acknowledged frontier is 995 on H7. r1 is H7/1000, r2 H7/990, and r3 sibling H6/1010.

**Reasoning.** r1 covers the required prefix on the accepted history. r2 would lose acknowledged positions 991–995. r3's larger number belongs to a divergent history and cannot be compared as freshness. Integrity/compatibility checks still apply to r1.

**Conclusion.** Eligibility requires history ancestry plus the required frontier, not maximum numeric position.

### Example 3

**Situation.** Three voters A, B, C use fixed membership. A and B elect x in term 9. Could y also win term 9?

**Reasoning.** Any majority has two voters. Another majority must intersect {A,B}. If each voter persists at most one term-9 vote before replying, the intersecting voter cannot vote for y, so y cannot collect two. If B forgets after restart, the proof fails.

**Conclusion.** Majority intersection yields uniqueness only with durable one-vote and fixed-membership premises.

### Example 4

**Situation.** Candidate r wins term 12 and the proxy routes new clients to it, but old primary p still holds storage credentials and runs scheduled billing jobs.

**Reasoning.** Proxy routing fences neither direct database access nor jobs. Install term-12 enforcement at database/storage mutation boundaries, revoke or rotate p's credentials, stop/fence its host or storage, and make jobs acquire/check the current epoch plus idempotent work IDs.

**Conclusion.** Fencing must cover every mutation surface, not only client discovery.

### Example 5

**Situation.** A planned switchover drains the old leader at frontier 4,200. Target has durably flushed 4,200 but replayed only 4,150.

**Reasoning.** If promotion can complete recovery before publication, wait for replay through 4,200, verify integrity, fence old writes, transfer authority, then publish. Publishing immediately could expose missing state or require foreground recovery. The exact order follows the engine protocol, but final-frontier coverage and fencing cannot be omitted.

**Conclusion.** Durable receipt alone is not always promotion readiness; the cut includes usable recovered state.

### Example 6

**Situation.** Client command `reserve-44` loses its response during promotion. The new leader contains a committed transaction with that command ID.

**Reasoning.** Query by stable ID and return the stored result. Issuing a new reservation may duplicate inventory allocation. If the ID is absent but the old divergent log has an uncertain commit, preserve a pending state until the recovery policy determines the chosen history and compensates any external effect.

**Conclusion.** Idempotent identity/status lookup is required across failover ambiguity.

### Example 7

**Situation.** Operators remove two unreachable members from a five-node configuration so two surviving nodes form a majority of a new two-node membership.

**Reasoning.** The unreachable three may still form a majority of the old membership and elect elsewhere. An uncoordinated configuration replacement creates disjoint decision quorums. Use the protocol's joint/overlapping membership change or an external disaster-recovery procedure that first fences the old configuration.

**Conclusion.** Editing membership to regain quorum can create two quorums unless configurations intersect or are fenced.

### Example 8

**Situation.** The former PostgreSQL primary returns after the standby was promoted and accepted writes on a new timeline.

**Reasoning.** Keep the former primary isolated, preserve evidence, identify the common ancestor and divergent transactions, and reconcile business outcomes. If `pg_rewind` prerequisites and required WAL hold, rewind it against the new primary and replay; otherwise reseed. Do not expose it as writer or copy relation files manually.

**Conclusion.** A former leader rejoins the chosen history through controlled rewind/reseed, never implicit failback.

### Example 9

**Situation.** A lease-based leader has a 30-second lease. Its clock is 12 seconds slow while the coordinator's expiry view differs.

**Reasoning.** If bounded-clock assumptions do not cover the error, the old leader can believe its lease valid after a new lease is granted. Use conservative expiry intervals and a resource-enforced fencing token; stop writes before local uncertainty reaches the bound. Without proven clock/delay bounds, do not base exclusivity solely on local lease time.

**Conclusion.** Lease safety depends on explicit time assumptions and usually benefits from monotonic fencing epochs.

### Example 10

**Situation.** Promotion restores writes in 40 seconds, but no replica covers the new leader, synchronous mode is disabled, and backups have not run.

**Reasoning.** Service recovery objective may be met, but the system is in a degenerate single-copy state. Prioritize new replica seeding, retained-log capacity, synchronous membership restoration, backup/archive verification, read-capacity recovery, and another failover drill. Track this as incident work, not ordinary backlog.

**Conclusion.** Failover completion includes restored protection, not only a responding endpoint.

## Cross-Program Connections

- Distributed Systems owns failure detectors, consensus, quorum intersection, leases, views, and replicated-state-machine safety; database failover must use rather than approximate those results.
- Systems Engineering owns hazard analysis and assurance across storage, power, network, identity, control-plane, and human failure domains.
- Platform Engineering owns service discovery, load balancing, credentials, node lifecycle, and orchestration; those controls must carry/enforce the database epoch.
- Software Delivery and Reliability Engineering owns runbooks, drills, incident modes, recovery objectives, evidence, and post-incident redundancy restoration.
- API and Service Engineering owns command idempotency and ambiguous outcome protocols exposed to clients during connection loss.
- Security Engineering owns authenticated membership, least privilege, credential revocation, protected fencing operations, and auditability of authority changes.

## References

1. PostgreSQL Global Development Group. [PostgreSQL 18: Failover](https://www.postgresql.org/docs/18/warm-standby-failover.html). Current promotion, external failure-management, old-primary fencing, and degenerate-state guidance checked 2026-09-05.
2. PostgreSQL Global Development Group. [PostgreSQL 18: `pg_promote`](https://www.postgresql.org/docs/18/functions-admin.html) and [`pg_ctl promote`](https://www.postgresql.org/docs/18/app-pg-ctl.html). Current promotion interfaces checked 2026-09-05.
3. PostgreSQL Global Development Group. [PostgreSQL 18: `pg_rewind`](https://www.postgresql.org/docs/18/app-pgrewind.html). Current timeline-divergence and rewind prerequisites checked 2026-09-05.
4. Oracle. [MySQL 8.4 Reference Manual: Using GTIDs for Failover and Scaleout](https://dev.mysql.com/doc/refman/8.4/en/replication-gtids-howto.html). Current GTID positioning and source-change behavior checked 2026-09-05.
5. Oracle. [MySQL 8.4 Reference Manual: Asynchronous Connection Failover](https://dev.mysql.com/doc/refman/8.4/en/replication-asynchronous-connection-failover.html). Current connection-source switching scope checked 2026-09-05.
6. Tushar Deepak Chandra and Sam Toueg. “Unreliable Failure Detectors for Reliable Distributed Systems.” *Journal of the ACM* 43(2), 1996. Failure-detector model and consensus relationships.
7. Diego Ongaro and John Ousterhout. [In Search of an Understandable Consensus Algorithm](https://raft.github.io/raft.pdf). USENIX ATC, 2014. Terms, durable votes, log freshness, and membership foundations.
8. Barbara Liskov and James Cowling. [Viewstamped Replication Revisited](https://pmg.csail.mit.edu/papers/vr-revisited.pdf). MIT CSAIL technical report, 2012. Views, primary changes, quorum state transfer, and recovery.
9. Cary G. Gray and David R. Cheriton. “Leases: An Efficient Fault-Tolerant Mechanism for Distributed File Cache Consistency.” ACM SOSP, 1989. Lease timing and authority foundations.
10. Jim Gray and Andreas Reuter. *Transaction Processing: Concepts and Techniques*. Morgan Kaufmann, 1993. Failures, recovery, transaction identity, and high-availability foundations.

## Exercises

### Exercise 1

Distinguish failure detection, eligibility, election, fencing, promotion, and routing. Give one unsafe outcome caused by skipping each of eligibility and fencing.

### Exercise 2

Membership has five voters. Under a fixed majority election, compute the majority size and prove that two candidates cannot both win one term if every voter durably votes once. Then identify two assumptions whose violation breaks the proof.

### Exercise 3

A failover controller promotes the reachable replica with the greatest numeric LSN, flips DNS, and later enables read-only mode on the old primary when it reconnects. Diagnose at least six independent hazards and propose a safe sequence.

### Exercise 4

Compare an external linearizable coordinator with a three-data-node integrated consensus election for a database. Discuss authority, data eligibility, failure domains, operational coupling, fencing, and testing; recommend when each is appropriate.

### Exercise 5

Design failover for a payment database spanning two zones plus a third-zone witness. Synchronous policy promises one remote durable copy. Include detection, candidate frontier/history checks, witness rules, term persistence, fencing all mutation paths, client ambiguity, service publication, old-primary rejoin, degraded-mode behavior, evidence, and fault tests.

## Answers to the Exercises

### Answer 1

**Failure detection** suspects loss from observations. **Eligibility** proves a candidate can safely serve the role from the required history/state. **Election** grants unique authority for a term. **Fencing** makes older authority ineffective. **Promotion** recovers and switches the chosen replica into writer mode/new history. **Routing** exposes only the ready current term to clients. Skipping eligibility can elect a stale, corrupt, incompatible, or sibling-history replica and lose acknowledged data. Skipping fencing can leave the old primary writable, producing split brain even if the election itself chose one new leader.

### Answer 2

A majority of five is $\lfloor5/2\rfloor+1=3$. Any two subsets of three among five intersect because two disjoint size-three subsets would require six distinct voters. Suppose x and y both win term e; their voting majorities intersect at voter v. If v persists at most one vote for e before acknowledging, it cannot vote for both, a contradiction. The proof fails if votes are forgotten/non-durable, identities are duplicated, voters use different membership configurations, one voter can grant twice, or messages/terms are unauthenticated and replayed.

### Answer 3

Hazards include numeric positions from divergent histories; no required acknowledged-frontier check; no integrity/compatibility/apply readiness; responsiveness mistaken for safety; DNS caches and direct connections; publication before fencing; old primary remains writable during partition; read-only later is bypassable and too late; no durable election term; no membership/witness decision; ambiguous client transactions; and no rejoin/redundancy plan.

A safe sequence declares the incident and limits write admission, gathers current membership/detection evidence, obtains exclusive durable authority for a new term, enforces and verifies fencing at storage/network/credential/job boundaries, evaluates candidates by accepted history plus required frontier/integrity/compatibility, completes chosen-history recovery, durably promotes/creates the term, enables only token-checked mutation paths, publishes readiness with the epoch, reconciles client transaction IDs, then isolates and rewinds/reseeds the old primary and restores redundancy. If no candidate covers the required frontier, remain unavailable or require explicit quantified data-loss authorization.

### Answer 4

An external linearizable coordinator centralizes terms, membership, and fencing tokens independently of database nodes. It can coordinate heterogeneous databases and survive data-node problems, but becomes an operational dependency whose own quorum, identity, region placement, leases, and outage modes require proof. It still needs database-specific eligibility and resource token enforcement; a lock cannot make stale data safe.

Integrated consensus couples election to replicated-log freshness and can prove the chosen leader contains committed entries under one protocol. It reduces semantic gaps but requires three or more well-placed data voters, correct durable term/vote/log behavior, and careful membership changes; slow data/storage nodes participate in control availability. Use integrated consensus when the engine truly implements and exposes its proof. Use an external coordinator for primary/standby engines lacking election when its linearizability and fencing can be trusted and eligibility is independently enforced. Neither is appropriate if mutation resources ignore epochs. Test partitions, restarts, membership, coordinator/data disagreement, stale candidates, and fence failure in both.

### Answer 5

Use authenticated data nodes A/B in distinct zones and witness W in a third, with one durable vote per term and a fixed/jointly changed membership epoch. Heartbeat/query/storage signals only trigger suspicion. To win, a candidate needs two of three durable votes, including its own, and must prove accepted history ancestry, integrity/compatibility, complete recovery, and durable/apply coverage through the greatest frontier promised by the source-plus-one-remote-flush policy. The witness never overrides data eligibility.

Before publishing the winner, install the new term at storage or another authoritative write boundary, power/storage/credential-fence the old leader when possible, revoke replication-source and job/consumer authority, and require term tokens on database writes, billing jobs, outbox dispatch, migrations, and sequence allocation. Persist election term/votes before replies and promotion history before readiness. Reset pools and publish the new endpoint with cluster/term metadata only after recovery and write probes pass.

Every payment command has an idempotency ID and durable status. Broken connections query the new chosen history before retry; uncertain old-history transactions remain in reconciliation, and external effects use an outbox/inbox. If neither data node covering the required frontier can win, protected writes stop; there is no automatic stale promotion. If the remote copy promise is explicitly weakened, record the term/frontier interval and restrict transaction classes.

Keep the old primary isolated, preserve logs, compare histories and payment IDs, then rewind it when supported or reseed it; never fail back directly. Completion requires a new protected replica, restored synchronous policy, backups/archives, and a follow-up failover test. Evidence records detector observations, votes, membership, candidate frontiers, fence results, promotion term/timeline, routes, ambiguous/lost IDs, and redundancy restoration. Tests cover asymmetric partitions, witness isolation, node pause, disk-full/corruption, stale and sibling candidates, forgotten votes, duplicate identities, delayed old automation, failed fence, cached endpoints, response loss, old-node restart, and second failure in degenerate mode; the oracle asserts one writable term and preservation of every covered acknowledged payment.
