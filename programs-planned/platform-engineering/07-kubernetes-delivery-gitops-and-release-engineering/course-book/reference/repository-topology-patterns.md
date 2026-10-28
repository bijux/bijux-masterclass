# Reference — Repository topology patterns

Monorepo and multirepo designs can both be sound. Evaluate source authority, environment approval, credential scope, blast radius, promotion ergonomics, history, and disaster recovery.

Environment directories simplify comparison but require path-level production controls. Environment branches isolate pointers but drift and can be rewritten. Atlas uses environment directories with immutable release references and separate production approval.

## Extended reader notes

A monorepo can provide atomic review across application and environment state, but it can also grant application contributors excessive production reach. Separate repositories can clarify authority and reduce credential scope, but they introduce cross-repository lineage and availability dependencies. Environment branches make promotion visually simple but often accumulate divergent histories. Directory-based environments simplify comparison but may give one commit authority over every environment.

Evaluate topology with concrete questions: which actor may write production desired state; how is artifact identity promoted; how are shared bases pinned; how is a release reverted without rewriting history; how are automation proposals reviewed; and what remains available during a repository outage.

Atlas uses conceptual separation even when files share one teaching repository. The application team owns source, the build system owns immutable artifacts, and environment owners approve desired revisions. Image automation writes only a candidate branch. Production lineage is a predecessor-linked release record, not an assumption that branch ancestry is always clean.
