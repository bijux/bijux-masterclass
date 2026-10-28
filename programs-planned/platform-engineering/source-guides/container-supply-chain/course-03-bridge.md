# Course 3 bridge — from cloud hosts to OCI releases

Course 2 can create compute, identity, networks, encryption, and durable data. It still assumes a machine-oriented application package. Course 3 changes the release boundary.

The Atlas workload becomes two OCI image indexes—API and worker—plus evidence attached to their immutable digests. Environment configuration, secrets, durable state, and cloud identity stay outside the images. The platform can now replace hosts without rebuilding the workload and can later ask Kubernetes to reconcile the same release.

The bridge is successful only when three identities remain separate:

```text
source identity
    commit or source digest

artifact identity
    OCI image/index digest

runtime identity
    workload principal and process UID/GID
```

Confusing these identities produces common failures: using a tag as release identity, embedding credentials to make a build work, or treating a signature as authorization to run.
