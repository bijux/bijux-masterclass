# Course 1 → Course 2 handoff

This directory is the immutable public-contract baseline consumed by
**Contract-Driven API Service Engineering**. It represents public API **1.1.0**
using OpenAPI **3.1.2**, with an OpenAPI **3.2.0** frontier copy for standards
study.

Course 2 may change application, database, worker, storage, and release
mechanisms, but it may not silently weaken this baseline. The manifest makes
that constraint machine-checkable.

Regenerate only after Course 1's proof route passes.
