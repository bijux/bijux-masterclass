# Graph gateway database ownership

The graph gateway owns only graph-operational metadata:

- released schema versions and their digests;
- trusted persisted-operation documents;
- client registrations and operation ownership;
- declared query budgets;
- subscription resume records when the chosen transport requires them.

It does **not** own project, dataset, analysis-run, artifact, delivery, tenant,
or authorization facts. Those remain with their Course 8 service owners. A
GraphQL resolver may call an owner through a released interface; it may not join
private service tables merely because a shared database is convenient in a
local laboratory.

The four migrations in this directory therefore create only platform-catalog
and graph-control structures. They deliberately do not copy domain tables. This
separation is a release and security property: deleting the graph gateway's
metadata database must make the graph interface unavailable, but it must not
destroy business truth.
