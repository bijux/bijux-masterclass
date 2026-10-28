# Guide — Argo CD native lane

The primary native lane uses one `AppProject`, environment `Application` resources, and an optional `ApplicationSet` for disposable clusters.

Verify in order:

1. repository and chart sources resolve to immutable revisions;
2. destination cluster and namespace fall within the Project;
3. generated manifests match the reviewed render digest;
4. the diff shows intended create, update, and prune actions;
5. sync options and field manager are recorded;
6. health rules observe current generation;
7. hooks and waves are idempotent and least privileged;
8. protected resources cannot be pruned;
9. application status and user/data gates remain separate.

Do not begin with the UI. Capture the Application YAML, controller status, resolved revision, resource tree, diff, Events, and Kubernetes managed fields. During a repository outage, verify that the Application reports source failure while running resources remain.

## Extended reader notes

The native Argo CD lane begins with the AppProject, because it defines the source, destination, kind, and role boundary. Then inspect each Application’s resolved revision, source plugin or renderer, generated set, inventory, diff, sync options, health rules, hooks, and prune scope.

Exercise three failures: repository unavailable, an application-owned field manually changed, and a protected resource removed from source. The first must retain last-known-good live state; the second should repair according to ownership; the third must be blocked by project and policy. Capture Application conditions, resource tree, Kubernetes managed fields, and Events.

Do not use the UI screenshot as the evidence artifact. Export the objects and bind them to the release subject.
