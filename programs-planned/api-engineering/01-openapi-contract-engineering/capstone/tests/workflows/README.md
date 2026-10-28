# Workflow evidence

The Arazzo description is validated against the bundled OpenAPI source by `make workflow`. Live conformance separately executes the same outcome: create a project, register and upload a dataset, start an idempotent run, observe completion, and retrieve artifacts.

Arazzo describes dependencies and value flow. It does not fabricate a workflow runner's ability to sleep until asynchronous work finishes or to receive a webhook. The workflow therefore models status retrieval as an explicit step and records asynchronous boundaries in its descriptions.
