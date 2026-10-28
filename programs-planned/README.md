# Planned programs

This directory preserves unfinished teaching material while it is developed and
reviewed. Inclusion here does not establish technical correctness, course
completion or readiness for learners.

Supported courses remain under `programs/`. Planned material is outside their
validation matrix, qualification fingerprints and published documentation
catalogue. Dependency-update configuration does not enroll these sources.
Repository governance and standards checks still apply to changes in this
repository.

## Retained material

| Collection | Contents | Provenance |
| --- | --- | --- |
| [Computing reference](computing-reference/README.md) | Thirty computing domains, existing chapters, module plans, validation tools and retained review records from Bijux Courses | [Preservation notes](computing-reference/PRESERVATION.md) and [source map](computing-reference/SOURCE.json) |
| [Node.js Programming](node-programming/README.md) | Six source courses with code, exercises and later-course outlines | [Collection status](node-programming/COLLECTION.md) and [source map](node-programming/SOURCE.json) |
| [Rust Programming](rust-programming/README.md) | Three source editions in Git history, a candidate tree and foundation notes | [Collection status](rust-programming/COLLECTION.md) and [source map](rust-programming/SOURCE.json) |
| [API Engineering](api-engineering/README.md) | Two source editions in Git history, candidate lessons and OpenAPI handoff fixtures | [Collection status](api-engineering/COLLECTION.md) and [source map](api-engineering/SOURCE.json) |
| [Platform Engineering](platform-engineering/README.md) | Seven source courses, their guides and supporting code | [Collection status](platform-engineering/COLLECTION.md) and [source map](platform-engineering/SOURCE.json) |
| [Dask](data-systems/dask/README.md) | Working chapter rewrite and both original Git revisions | [Collection status](data-systems/dask/COLLECTION.md) and [source map](data-systems/dask/SOURCE.json) |
| [Polars](data-systems/polars/README.md) | Working chapter rewrite and both original Git revisions | [Collection status](data-systems/polars/COLLECTION.md) and [source map](data-systems/polars/SOURCE.json) |
| [Python Extensions](python-programming/README.md) | Systems, parallel, metaprogramming, foundation and patterns material | [Collection status](python-programming/COLLECTION.md) and [source map](python-programming/SOURCE.json) |
| [Algorithm Engineering](algorithm-engineering/README.md) | Hash collections, asymptotic analysis, invariants and algorithm notes | [Collection status](algorithm-engineering/COLLECTION.md) and [source map](algorithm-engineering/SOURCE.json) |
| [Programming Language Theory](programming-language-theory/README.md) | Lambda-calculus chapters and outline | [Collection status](programming-language-theory/COLLECTION.md) and [source map](programming-language-theory/SOURCE.json) |
| [Research Workflows](research-workflows/README.md) | Testing, delivery, data tooling, orchestration and HPC material | [Collection status](research-workflows/COLLECTION.md) and [source map](research-workflows/SOURCE.json) |

The source collection has its own historical completion labels. Those labels are
preserved source claims; they do not qualify the material as supported Masterclass
courses. Missing chapters remain plans. Draft chapters remain drafts.

## Working with planned material

Keep each collection's teaching content, supporting code and provenance together.
Record the origin of additional material and preserve useful differences before
replacing an earlier edition. Keep generated run output in the repository-root
`artifacts/` directory. Historical review records already retained with the source
are maintained evidence, not a destination for new run output.

Do not connect a supported course to planned implementation files. Execution-input
collection rejects symlinks into this directory. Any shared implementation needed
by a supported course must first have an appropriate supported owner.

Backlogs, execution prompts and assistant instructions remain outside the product
tree. Their presence in an original historical commit does not make them current
repository instructions.

## Promoting material

Promote one coherent course or reference collection when its intended audience,
prerequisites, learning outcomes and authored scope are clear. Review the actual
lessons, exercises, answers, references and any runnable examples. Record what was
tested and any remaining limits.

Move accepted material to its supported owner, register its documentation and
validation routes, update the appropriate family index, and run the affected
checks. Preserve its source identities and Git history. Promotion does not require
finishing every other planned course or every entry in the original roadmap.
