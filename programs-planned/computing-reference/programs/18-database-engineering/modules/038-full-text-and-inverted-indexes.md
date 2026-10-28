---
module_id: DBE-038
program: Database Engineering
level: 1
module_number: 38
title: Full-Text and Inverted Indexes
status: complete
last_verified: 2026-08-30
---

# Full-Text and Inverted Indexes

## One-Page Review

### Governing question

How does a database turn text into searchable terms and postings while preserving the declared language, Boolean, phrase, ranking, visibility, update, and authorization semantics across analyzer and index versions?

### Essential definitions

An **analyzer** transforms input through character normalization, tokenization, token filters, stop-word handling, and possibly stemming/lemmatization into indexed **terms/lexemes** with positions and fields. A **term dictionary** maps each term to metadata and a **posting list** of document/row identifiers; postings may carry frequency, positions, field/weight, and payload. An **inverted index** maps terms to documents—the reverse of a forward document-to-terms representation. Boolean retrieval intersects/unions/differences posting sets. A **phrase query** joins positional postings with declared gaps/order. **Document frequency** is the number of documents containing a term; **term frequency** counts occurrences within one document. A **ranking function** orders candidates by an explicitly versioned score such as BM25 plus business signals. A **pending list/segment** batches writes before merge. A **recheck** validates lossy candidates, row visibility, and residual predicates against authoritative content.

### Central model, mechanism, or theorem

Index-time and query-time analyzers must emit compatible term streams. For exact Boolean AND, every qualifying document belongs to every required posting list, so intersecting lists is sound; OR uses union. Phrase correctness additionally requires position sequences satisfying adjacency/gap constraints. Ranking is applied to a complete candidate set using consistent corpus/document statistics and deterministic tie-breaking for pagination. Physical postings may contain dead/stale candidates under MVCC or asynchronous indexing, but final results must obey the system's documented consistency, visibility, tenant, and authorization contract.

### Critical invariants

- Analyzer configuration, language, normalization, tokenizer, filters, stop words, stemmer, field mapping, and version are explicit and compatible between indexing/querying.
- Every searchable term occurrence creates the required posting with correct document identity, frequency, position, field, and generation.
- Boolean set operations run over compatible index snapshots and document-ID universes; NOT has a declared live universe.
- Phrase/proximity queries never infer order from term presence alone; positions or authoritative recheck establish it.
- Lossy/prefix/trigram/signature candidates are rechecked where the access method cannot prove exact text semantics.
- Ranking inputs and formula/version are consistent; floating ties use a stable secondary key and continuation token.
- Row/document visibility, deletion, tenant, ACL, embargo, and residual policy are enforced before return and before sensitive snippets/facets.
- Inserts, updates, deletes, pending lists, segments, merges, vacuum, WAL, replicas, and external pipelines preserve the stated freshness/no-loss contract.
- Analyzer/schema/statistics/model changes trigger compatible dual-read/reindex migration rather than reinterpret old postings silently.
- Query parsing and execution enforce grammar, escaping, clause/expansion/depth/time/memory/result limits.

### Common failures

Failures include calling substring `LIKE '%x%'` full-text search; tokenizing documents and queries differently; treating case folding as full Unicode/language analysis; removing a stop word needed for phrase semantics; stemming proper nouns incorrectly; using term presence for a phrase; applying NOT without a live universe; returning dead/invisible/unauthorized postings; believing ranking scores are probabilities; paginating unstable tied scores; using stale document-frequency statistics without labeling; allowing prefix/fuzzy expansion to explode; rebuilding with a new analyzer in place; desynchronizing SQLite external-content FTS; assuming GIN pending-list speed removes merge cost; and logging raw sensitive queries/snippets.

### Compact example

Four tiny documents use a declared ASCII lowercase/alphanumeric analyzer. Postings for `database` are documents 1 and 3; postings for `systems` are 1,3,4, so AND candidates are `(1,3)`. Document 3 is deleted/invisible, leaving result `(1)`. Only document 1 has positions where `database` is immediately followed by `systems`. A toy `text search` frequency score ranks document 4 (three occurrences) above documents 1 and 2 (two each), with document ID breaking the tie. This demonstrates mechanics, not linguistic quality or production relevance.

### Connections

This module extends [DBE-037](037-bitmap-and-brin-style-indexes.md)'s posting-set algebra and recheck discipline. DBE-039 covers index write amplification; DBE-040 chooses indexes from workload evidence. Later query-processing modules cover ranking/Top-K execution and external systems cover distributed search.

## Governing Question

Full-text correctness begins before the index. What counts as a term in English prose, source code, email, CJK text, emoji, hyphenation, or biomedical nomenclature differs. Query syntax may mean literal words, Boolean clauses, phrases, prefixes, fuzzy variants, or field scopes. The data structure cannot repair an undefined linguistic/search contract.

The governing question therefore asks which document/query representations are created, which matching relation follows, which scores/order are promised, and how those representations remain transactionally and operationally aligned with authoritative rows. “Has an inverted index” is not a user-visible semantics.

## Why This Matters

Text predicates occur in catalogs, tickets, logs, documentation, messaging, and discovery. A B+ tree orders whole scalar strings; it cannot efficiently enumerate documents containing arbitrary interior terms. An inverted index makes cost proportional to term/posting behavior instead of scanning/tokenizing every document per query.

Search also creates correctness and security obligations. Analyzer changes alter recall. Ranking changes alter pagination and business exposure. Stale deletes can leak private content. A broad OR/prefix/fuzzy query can consume unbounded CPU/memory. The index must be treated as a governed derived-data product, not a magical relevance feature.

## Prerequisites and Retrieval

Retrieve sets/bitmaps and no-false-negative rechecks from [DBE-037](037-bitmap-and-brin-style-indexes.md), expression/version semantics from [DBE-036](036-partial-and-expression-indexes.md), MVCC/storage/recovery from DBE-021–030, and composite/covering design from [DBE-035](035-composite-and-covering-indexes.md).

Before continuing, intersect sorted integer lists, merge-union them without duplicates, and positional-join two lists where the second position equals the first plus one. Explain Unicode normalization versus case folding versus stemming, and why authorization is not just another relevance feature.

## Learning Objectives

After completing this module, you should be able to:

1. specify an analyzer pipeline for documents and queries with explicit language/version semantics;
2. construct a term dictionary and postings with frequency, positions, fields, and document identity;
3. derive Boolean AND/OR/NOT and phrase/proximity retrieval;
4. distinguish exact postings, expansion candidates, lossy matches, visibility, and residual rechecks;
5. explain TF, DF/IDF, BM25-style scoring, field boosts, tie-breaking, and score limitations;
6. reason about postings compression, skips, dictionaries, prefix/fuzzy expansion, and Top-K execution;
7. trace transactional updates, pending lists/segments, merges, deletes, vacuum, WAL, and asynchronous freshness;
8. version and migrate analyzer/schema/ranking changes without silently mixing semantics;
9. enforce tenant/ACL/query-complexity/privacy boundaries; and
10. validate search with golden analysis, differential recall, ranking judgments, failure tests, and operational metrics.

## Core Exposition

Define the document schema first. A document may concatenate title, tags, abstract, and body, but field boundaries and weights matter. Stable document identity must connect postings to an authoritative row/version. Decide which fields are searchable, retrievable for snippets, filterable, sortable, and security-sensitive. Avoid indexing secrets merely because access filtering exists later.

The analyzer consumes characters and emits `(term,position,field,offset,payload)` as required. Character filters may normalize Unicode or markup. The tokenizer declares boundaries. Token filters lowercase/case-fold, remove stop words, stem/lemmatize, expand synonyms, or emit n-grams. Position increments must preserve gaps when stop words disappear if phrase semantics depend on original distance. Offsets support highlighting but must map back to the same source/version.

Language matters. Whitespace tokenization fails languages without word separators. Naive lowercasing differs from Unicode case folding and locale-specific rules. Stemming increases recall but can collapse distinct words; lemmatization needs language knowledge. N-grams help CJK/prefix/substrings at larger posting volume. Code identifiers may need camel/snake splitting while retaining the original token. Use analyzers per field/language rather than one global folklore pipeline.

At indexing, accumulate terms per document. For each unique term, append a posting sorted by document ID. Store term frequency and positions when ranking/phrases need them. The dictionary can be a B-tree/FST/hash-like structure; frequent terms outgrow inline postings into posting trees/blocks. Delta-encode document IDs and positions, then variable-byte/bit-pack/compress blocks. Skip data permits intersection to jump over ranges.

Boolean AND intersects sorted postings, preferably beginning with the shortest/rarest. OR merge-unions. NOT subtracts from a declared candidate/live universe and is usually anchored by positive clauses; a pure global NOT is broad. Duplicate terms/clauses should be normalized without changing boosts/phrase positions. Parentheses and operator precedence belong to the public query grammar.

Phrase query `a b` requires a document present in both postings and some position `p` for `a` with `p+1` for `b`, adjusted for analyzer position increments. Proximity allows a bounded window/order. If positions are omitted to shrink the index, exact phrase search needs content recheck or is unsupported. Term conjunction alone returns documents with words far apart or reversed.

Prefix queries enumerate dictionary terms sharing a prefix or use dedicated prefix/n-gram postings. Wildcard/regex/fuzzy search may enumerate an automaton over the dictionary. Expansion can dominate cost and skew ranking; cap term count, states, edit distance, Boolean clauses, time, memory, and results. Never implement arbitrary regex by silently scanning all indexed terms without a resource contract.

Postings can be exact for analyzer terms yet still yield candidate rows requiring MVCC/deletion/ACL/residual checks. Lossy GIN operator classes, trigrams, prefixes, signatures, external-index lag, or stale deletes add rechecks. Separate `posting_candidates`, `text_matches`, `visible`, `authorized`, and `returned`. Facets/snippets must use the authorized set or they can leak counts/content.

Ranking turns matching into an order, not truth. Term frequency rewards repetition; inverse document frequency rewards rarer terms, commonly `idf(t)=log((N-df(t)+0.5)/(df(t)+0.5)+1)` in BM25 variants. BM25 saturates TF and normalizes document length using parameters `k1,b`. Field boosts, freshness, popularity, quality, personalization, and learning-to-rank signals may follow. Declare exact formula, corpus/statistics snapshot, parameters, feature transformations, and tie-break.

Scores are usually not comparable across indexes, shards, corpus/statistics versions, queries, or ranking models. Normalizing into 0–1 does not make probabilities. Approximate Top-K algorithms can skip low-impact postings using upper bounds, but must state exact/approximate guarantees. Stable pagination uses `(score,document_id)` plus snapshot/index/ranker version; recalculated scores can otherwise duplicate/skip results.

PostgreSQL full-text search illustrates analyzer/query types: text becomes `tsvector` lexemes with optional positions/weights; query constructors produce `tsquery` with AND/OR/NOT/phrase operators; ranking functions are application-tunable examples. PostgreSQL GIN stores keys with posting lists/trees and is commonly preferred for text search. These mechanisms are product-specific, not a universal grammar/ranker.

SQLite FTS5 exposes tokenizer, prefix, detail, column-size, content, phrase/NEAR, and BM25-related choices. Its official documentation warns that external-content indexes depend on the application/triggers to keep the FTS index consistent with the content table. A consistency failure can yield unpredictable results. This is a concrete example of why derived-index ownership matters.

MySQL full-text behavior depends on storage engine/parser/mode. Current official documentation distinguishes natural-language and Boolean syntax, minimum/maximum token sizes, stop lists, built-in versus n-gram/MeCab parsing, and engine-specific operators. Changing token-size/stopword/parser configuration requires rebuilding compatible indexes; never generalize settings across products.

Updates are multi-valued. In-place modification logically removes old document terms and adds new terms. MVCC may retain old-version postings until cleanup. Direct posting edits scatter random writes, so engines batch in pending lists or immutable segments. Queries consult main plus pending segments; merges compact/sort postings and purge deletes. Batching improves foreground writes but shifts latency, memory, WAL, and space into flush/merge spikes.

PostgreSQL GIN's fast-update pending list illustrates this trade. A large pending list can slow queries and cleanup can cause foreground spikes; vacuum/autovacuum and configuration affect cleanup. Segment-based external engines similarly need merge policies and tombstones. Monitor debt rather than calling buffered writes free.

Transactional database indexes can share WAL/MVCC, though access-method visibility rules still apply. An external search service usually receives changes through an outbox/change stream and is eventually consistent. Define acknowledged-write-to-search latency, ordering/idempotence, delete/tombstone handling, replay, backfill, dual-write prohibition, lag/error DLQ, rebuild, reconciliation, and query behavior during lag.

Analyzer changes are schema migrations. Build a new index version from authoritative content, dual-write/replay, compare document/term counts and shadow queries, evaluate relevance/recall/security, catch up, atomically switch an alias/catalog pointer, retain rollback, then retire old state. Mixing postings built by two analyzers under one dictionary makes query semantics incoherent.

Security starts at query parsing. Use structured query APIs or escape user text; do not concatenate into expert grammar. Enforce tenant/ACL before ranking/faceting/snippets when possible and always before return. Bound pathological clauses/expansions/highlighting. Redact query logs, hash/sample identifiers, apply retention, and treat search terms as sensitive behavioral data.

Observability records analyzer/index/ranker versions, freshness watermark/lag, document/term/posting/deleted counts, dictionary and posting-block sizes, pending/segment count/bytes/age, flush/merge/vacuum time, query parse/rewrite terms, per-term DF, candidates/intersections/skips/expansions, rechecks, visible/authorized/returned, ranking/Top-K work, cache/I/O, timeout/cancellation, recall judgments, p50/p99, and resource-limit rejections. Avoid raw content.

Testing has four oracles. **Analysis:** golden token/position/offset streams across Unicode/languages/settings. **Retrieval:** compare Boolean/phrase/prefix results to a slow reference analyzer over authoritative documents, including deletes/updates/MVCC. **Ranking:** judged query sets, NDCG/MRR/recall/precision with significance and slice analysis, not one demo. **Operations:** crashes during pending flush/merge, replay, lag, duplicate/out-of-order changes, analyzer migration, corruption, cancellation, authorization, and adversarial query limits.

The executable model uses ASCII lowercase/alphanumeric tokens, no stop words/stemming/Unicode, exact positions, in-memory postings, visibility filtering, exact Boolean/phrase logic, and a toy frequency rank with document-ID tie-break. It demonstrates mechanics only—not BM25, language quality, MVCC, persistence, authorization, concurrency, WAL, compression, or performance.

<!-- bijux-verify: {"id":"inverted-index-retrieval","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"terms=('database', 'index', 'phrase', 'rank', 'recovery', 'search', 'supports', 'systems', 'text')\nand_candidates=(1, 3)\nand_visible=(1,)\nphrase_database_systems=(1,)\nor_phrase_rank=(2, 4)\nrank_text_search=((4, 3), (1, 2), (2, 2))\ninvariants=True\n","stderr":""}} -->
```python
documents = {
    1: {"text": "database systems index text search", "visible": True},
    2: {"text": "text index supports phrase search", "visible": True},
    3: {"text": "database recovery systems", "visible": False},
    4: {"text": "search search systems rank text", "visible": True},
}


def analyze(text: str) -> tuple[str, ...]:
    lowered = text.lower()
    normalized = "".join(
        character if "a" <= character <= "z" or "0" <= character <= "9" else " "
        for character in lowered
    )
    return tuple(token for token in normalized.split() if token)


postings: dict[str, dict[int, tuple[int, ...]]] = {}
for document_id, document in documents.items():
    positions: dict[str, list[int]] = {}
    for position, term in enumerate(analyze(str(document["text"]))):
        positions.setdefault(term, []).append(position)
    for term, term_positions in positions.items():
        postings.setdefault(term, {})[document_id] = tuple(term_positions)


def term_documents(term: str) -> set[int]:
    return set(postings.get(term, {}))


def phrase(first: str, second: str) -> tuple[int, ...]:
    candidates = term_documents(first) & term_documents(second)
    matches = []
    for document_id in sorted(candidates):
        first_positions = postings[first][document_id]
        second_positions = set(postings[second][document_id])
        if any(position + 1 in second_positions for position in first_positions):
            matches.append(document_id)
    return tuple(matches)


and_candidates = tuple(sorted(term_documents("database") & term_documents("systems")))
and_visible = tuple(
    document_id for document_id in and_candidates if documents[document_id]["visible"]
)
or_phrase_rank = tuple(sorted(term_documents("phrase") | term_documents("rank")))
scores = []
for document_id, document in documents.items():
    if not document["visible"]:
        continue
    tokens = analyze(str(document["text"]))
    score = tokens.count("text") + tokens.count("search")
    if score:
        scores.append((document_id, score))
ranked = tuple(sorted(scores, key=lambda item: (-item[1], item[0])))
phrase_match = phrase("database", "systems")
all_occurrences = sum(len(positions) for posting in postings.values() for positions in posting.values())
token_count = sum(len(analyze(str(document["text"]))) for document in documents.values())
invariants = all_occurrences == token_count and phrase_match == (1,) and 3 not in and_visible

print(f"terms={tuple(sorted(postings))}")
print(f"and_candidates={and_candidates}")
print(f"and_visible={and_visible}")
print(f"phrase_database_systems={phrase_match}")
print(f"or_phrase_rank={or_phrase_rank}")
print(f"rank_text_search={ranked}")
print(f"invariants={invariants}")
```

## Definitions and Notation

Let corpus `D`, analyzer `A_v`, term stream `A_v(d)`, posting `P_t={(d,tf,positions,fields,payload)}`, document count `N`, document frequency `df_t=|{d:t∈d}|`, term frequency `tf(t,d)`, and visible/authorized set `V`. Boolean candidates use postings; results are candidates intersected with `V` and residual semantics.

For a common BM25 form, `score(D,Q)=sum_t IDF(t) * tf(t,D)*(k1+1)/(tf(t,D)+k1*(1-b+b*|D|/avgdl))`, possibly multiplied/combined with field/business signals. Formula variants differ; declare IDF, parameters, corpus/statistics, boosts, and tie-break. The executable model instead uses an explicitly labeled integer occurrence count.

## Mechanisms, Invariants, or Proof Structure

A defensible search workflow is:

1. Bind tenant/auth/snapshot, document schema, analyzer/index/ranker versions, query grammar, and resource limits.
2. Parse then analyze query fields with compatible configuration; reject/escape invalid expert syntax.
3. Resolve exact/prefix/fuzzy terms within expansion limits and retrieve compatible postings/segments/pending state.
4. Plan intersections from selective inputs; union/subtract with a declared universe; positional-join phrases/proximity.
5. Recheck lossy text predicates, authoritative row version/visibility, tenant/ACL, and residual filters.
6. Score complete eligible candidates with declared statistics/model; use safe upper bounds only under stated exact/approximate contract.
7. Produce stable `(score,id)` order/continuation, authorized facets and source-version-aligned snippets.
8. Account freshness, candidates/rechecks, expansions, skips, ranking work, memory/I/O, timeout, and limitations.

Boolean soundness follows from set algebra when every qualifying analyzed term occurrence is present in compatible postings. Phrase soundness additionally follows from a positional witness meeting order/gap. Completeness fails if analyzer versions differ, postings are missing, or freshness contract allows lag; exact system claims must include those premises. This is a proof sketch, not a relevance proof—relevance is empirically judged.

## Alternatives and Trade-Offs

A database-native text index simplifies transaction/backup/authorization joins but may offer narrower linguistic/scaling/ranking features. An external engine offers analyzers, distributed segments, Top-K, facets, and operations at consistency/infrastructure cost. B+ tree serves exact/prefix under collation; trigram indexes serve substring/fuzzy candidates; vector search serves semantic similarity but not exact lexical/Boolean guarantees. Hybrid lexical-vector ranking adds fusion/calibration complexity.

Positions improve phrases/proximity/highlighting but enlarge postings. Frequencies enable ranking; omitting detail shrinks storage but removes features/requires recheck. Stop words shrink common postings but alter phrase/recall. Stemming raises recall and changes precision. Prefix n-grams accelerate prefixes at write/space cost. Pending lists/segments improve ingest throughput while moving cost to query/merge debt.

## Failure Modes and Misconceptions

- “Token equals word.” Language, Unicode, code, emoji, markup, and domain rules disagree.
- “Lowercase is normalization.” Case folding, Unicode form, accents, and morphology remain.
- “AND proves phrase.” Positions/order/gaps are required.
- “Stop words never matter.” Phrase, legal, code, names, and negation may depend on them.
- “Stemming only improves recall.” It can collapse distinct meanings and hurt precision.
- “Index hit is visible/authorized.” MVCC, deletion, tenant, ACL, and residual checks intervene.
- “BM25 score is probability.” It is a ranking score under a formula/statistics version.
- “Scores paginate stably.” Ties and statistic/index changes need ID/version continuation.
- “Fuzzy/prefix is cheap.” Dictionary expansion requires strict resource bounds.
- “Buffered writes are free.” pending-list/segment merges create debt and spikes.
- “External content stays synchronized.” Ownership/reconciliation is mandatory.
- “Analyzer upgrade is configuration.” It changes every derived term and requires migration.
- “Search replicas are instantly current.” Publish a measurable freshness contract.
- “Facets/snippets are harmless.” They can leak unauthorized counts/content.

## Worked Examples

### Example 1

`rats` may normalize to `rat` under an English stemmer but remain `rats` under a simple analyzer. If documents and query use different configurations, a valid result is missed. Conclusion: analyzer version is part of index semantics.

### Example 2

Postings `database={1,3}` and `systems={1,3,4}` intersect to `{1,3}`; visibility removes deleted 3. Conclusion: Boolean posting candidates are not final rows.

### Example 3

Document 1 has database at 0 and systems at 1; document 3 has positions 0 and 2. AND matches both, exact phrase matches only 1. Conclusion: positions distinguish conjunction from phrase.

### Example 4

Removing stop word `to` while collapsing position gaps makes phrase “go to school” incorrectly behave like “go school.” Preserve increments or define stop-word phrase semantics. Conclusion: discarded terms can still affect positions.

### Example 5

Prefix `a*` expands to 100,000 terms and unions huge postings. A three-character prefix index/limit may help; rejecting the query may be correct policy. Conclusion: expansion is a bounded execution problem.

### Example 6

BM25 ranks rare `quasar` more strongly than common `system`; a field boost favors title. A popularity feature then dominates. Without versioned formula/features, explanations and pagination drift. Conclusion: ranking is an owned model.

### Example 7

A GIN pending list grows under bulk ingest. Writes are fast, then a cleanup merge spikes latency and queries consult more state. Conclusion: observe deferred work, not just foreground inserts.

### Example 8

An external search index receives update v3 before delayed v2. Without per-document version checks, old content overwrites new. Idempotent ordered application/reconciliation rejects v2. Conclusion: asynchronous indexing needs version semantics.

### Example 9

Authorization removes document 9 after lexical scoring, but a facet counted its confidential project. Applying ACL only to hits still leaks. Conclusion: all derived outputs require authorization-safe candidate domains.

### Example 10

Analyzer v2 changes CJK bigrams. Build a new index, replay/dual-write, shadow compare recall/latency/security, catch up, switch versioned alias, retain rollback. Conclusion: analyzer change is a data migration.

## Cross-Program Connections

- [Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md) supplies dictionaries, postings, compressed lists, and skip intersections.
- [Algorithm Engineering](../../16-algorithm-engineering/ROADMAP.md) supplies set/positional joins, Top-K, and complexity bounds.
- [Data Engineering](../../19-data-engineering/ROADMAP.md) supplies derived-state pipelines, replay, watermark, reconciliation, and backfill.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) supplies query injection/DoS, ACL filtering, and privacy-safe telemetry.
- [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) supplies replication, segment/shard statistics, versioned delivery, and consistency.

## References

1. PostgreSQL Global Development Group, [Controlling Text Search](https://www.postgresql.org/docs/current/textsearch-controls.html), current parsing, lexemes, query forms, positions, weights, ranking, and highlighting.
2. PostgreSQL Global Development Group, [GIN Indexes](https://www.postgresql.org/docs/current/gin.html), current key/posting-list/tree implementation and operator-class interface.
3. PostgreSQL Global Development Group, [System Administration Functions: Index Maintenance](https://www.postgresql.org/docs/current/functions-admin.html#FUNCTIONS-ADMIN-INDEX), current `gin_clean_pending_list` behavior and operational cleanup interface.
4. SQLite Project, [FTS5 Extension](https://www.sqlite.org/fts5.html), official tokenizer, phrase/NEAR/prefix, BM25, detail, content, and merge behavior.
5. Oracle, [MySQL 8.4 Natural Language Full-Text Searches](https://dev.mysql.com/doc/refman/8.4/en/fulltext-natural-language.html), current parser, token-size, stopword, engine, and language guidance.
6. Oracle, [MySQL 8.4 Boolean Full-Text Searches](https://dev.mysql.com/doc/refman/8.4/en/fulltext-boolean.html), current Boolean grammar and engine-specific restrictions.
7. Christopher D. Manning, Prabhakar Raghavan, and Hinrich Schütze, [Introduction to Information Retrieval](https://nlp.stanford.edu/IR-book/), Cambridge University Press, 2008, inverted indexes, postings, compression, scoring, and evaluation.
8. Stephen Robertson and Hugo Zaragoza, [The Probabilistic Relevance Framework: BM25 and Beyond](https://www.staff.city.ac.uk/~sbrp622/papers/foundations_bm25_review.pdf), *Foundations and Trends in Information Retrieval* 3(4), 2009.
9. Apache Lucene Project, [File Formats](https://lucene.apache.org/core/10_3_1/core/org/apache/lucene/codecs/lucene103/package-summary.html), current segment, terms, frequencies, positions, and skip-data format documentation.
10. Justin Zobel and Alistair Moffat, [“Inverted Files for Text Search Engines”](https://doi.org/10.1145/1132956.1132959), *ACM Computing Surveys* 38(2), 2006, construction, compression, and query evaluation survey.

## Exercises

### Exercise 1

Analyze five multilingual/domain strings under two declared pipelines. Produce tokens, positions, offsets, stop/stem decisions, and identify recall/precision/phrase differences.

### Exercise 2

Given sorted postings with positions/frequencies, compute Boolean `(a AND b) OR c`, `a AND NOT b`, phrase `a b`, ordered proximity within three, and a stable visible result order.

### Exercise 3

Compute a declared BM25 variant for three documents and two terms from supplied TF, DF, lengths, `N`, `avgdl`, `k1`, and `b`; add a title boost, explain ties, and design continuation state.

### Exercise 4

Design a crash/concurrency-safe update path using pending lists or immutable segments with MVCC/deletes, WAL/commit, flush, merge, tombstones, replicas, corruption, and recovery.

### Exercise 5

Design a production evaluation and migration from analyzer/ranker v1 to v2, including golden analysis, retrieval oracle, relevance/security judgments, shadow traffic, backfill/catch-up, freshness, cutover, rollback, and limits.

## Answers to the Exercises

### Answer 1

A complete answer declares Unicode normalization/case fold, tokenizer/language, stop list, stemmer/ngram, field, and version before output. Include examples such as composed/decomposed accents, Turkish I, CJK without spaces, `snake_caseHTTP2`, apostrophe/hyphen, emoji, and a proper noun. Record each emitted term with original offset and position increment; do not invent one universal correct stream. Compare exact query streams: stop removal changes phrase gaps, stemming merges variants but may conflate names, n-grams improve CJK/prefix recall at posting cost, and code splitting improves component recall while retained originals support exact identifiers. Grade by internal analyzer/query consistency and explicit trade-offs.

### Answer 2

Intersect a/b by advancing the smaller document IDs; union the result with c without duplicates. For NOT, subtract b only from the declared positive/live universe—normally anchor with a. Phrase candidates first intersect documents, then keep a document if some `pos_b=pos_a+1`; ordered proximity-three accepts `1<=pos_b-pos_a<=3`. Apply visibility/ACL/residual filters after posting evidence (or earlier safe filters), then sort by the declared score and unique document-ID tie-break. A full answer shows pointer advances/positional witnesses and never uses term presence as phrase proof.

### Answer 3

Use exactly the chapter's declared IDF and BM25 saturation/length formula; compute each term contribution with intermediate IDF, denominator, TF fraction, then sum. Apply title boost only to specified occurrences/field score, not twice. Floating differences need tolerance and a deterministic document-ID secondary order. Continuation stores query/analyzer/index/statistics/ranker versions plus last `(score,id)` and snapshot/freshness boundary. Scores are ranking values, not probabilities; changing corpus statistics can reorder pages, so either bind a stable search snapshot/version or document restart/eventual behavior. Numeric answers depend on the exercise's supplied table and must reproduce it independently.

### Answer 4

Bind row/document generation and transaction. On commit, WAL/log an idempotent old-term deletion/tombstone plus new analyzed postings, or emit a versioned outbox event after authoritative commit. A pending list is query-visible under snapshot rules; flush writes sorted immutable segment/posting blocks and atomically publishes a manifest before retiring pending state. Merge reads immutable inputs, applies versioned tombstones, writes/checksums output, publishes manifest atomically, then reclaims inputs after readers/replicas release generations. Crash before publication keeps old manifest; after publication replays/recognizes new generation; repeat recovery is idempotent. Corruption quarantines/rebuilds from authoritative content. Test reordered/duplicate events, concurrent updates/deletes/search, disk-full, cancellation, replicas, and cleanup horizons.

### Answer 5

Freeze v1/v2 analyzer, schema, ranking formula/features/statistics contract, query grammar, and limits. Golden-test token/position/offset streams across languages and adversarial inputs. Build v2 from authoritative versioned content while dual-writing/replaying; reconcile document generations, counts, term/posting totals, deletes, tenant/ACL, and freshness watermark. Shadow representative queries and compare full result correctness, recall/precision/NDCG/MRR, slices, authorized facets/snippets, latency, candidates, expansions, memory/I/O, merge debt, and limit rejection. Human judgments are blinded/versioned with inter-rater/uncertainty reporting. Catch up to cutover watermark, atomically switch versioned alias, monitor, retain v1/replay for rollback, then retire after evidence window. Never mix analyzers in one index or call offline relevance gains production safety.
