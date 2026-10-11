# Catalogue source planning

The catalogue is derived from authored `programs/` Markdown and course navigation, the root `mkdocs.yml`, and its captured `mkdocs.shared.yml`. Generated `docs/` catalogue pages and `artifacts/mkdocs.root.yml` are outputs, not original tracked inputs.

`source_plan.build_plan(captured_bytes, environment=...)` is the pure boundary. It returns immutable original-to-public document mappings, exact projected content bytes, source hashes, and a derived configuration with its tracked owner and explicit configuration inputs, six current navigation owners, and only explicitly supplied environment values referenced by authored `!ENV` tags. It performs no filesystem, Git, process environment or clock reads. Pass relevant environment values explicitly; omitted values stay absent in the recorded input and use each authored YAML fallback independently on replay. The plan preserves the catalogue's existing Markdown and HTML hyperlink transformations and course order.

`files.capture_sources(root)` reads regular original inputs and generator code. `files.write_documents` and `files.write_configuration` recheck that capture before and after materialization. Configuration materialization requires complete matching documents. `files.verify_outputs` rejects missing, extra, modified or symlinked outputs and a configuration that differs from the plan. `files.verify_sources` rejects changed original or generator bytes. Filesystem capture rejects symlinked originals, and planning rejects unsafe paths, duplicate source/destination ownership and navigation without a planned document. Configuration writes reject hardlinked destinations and atomically replace the output inode. Existing family/library files outside the current plan are rejected before deleting any generated output; callers may supply exact reviewed prior output bytes through `previous_outputs` when intentionally retiring old generated paths. Generated-tree placement alone does not prove removal ownership.

The existing commands use this shared plan:

```sh
python scripts/sync_series_docs.py
python scripts/render_root_mkdocs.py
python -m unittest discover -s tests -p test_catalog_source.py
```

The public link helper names remain available from `scripts.sync_series_docs` for existing callers. New planning code belongs here and is selected by the existing series-site validation classifier.

Source hashes identify current bytes, not Git history or a publication approval. A production reconstruction must independently bind these inputs to its captured committed source, recheck output bytes, and review its native renderer/history capability. This module does not invent modification dates, mark generated files tracked, admit arbitrary commands, or approve a producer profile.
