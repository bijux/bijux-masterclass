# Module 6 — Configuration, secrets, and workload identity projection

Course 3 deliberately kept environment configuration, secret values, and cloud identity out of OCI image layers. Kubernetes can project runtime data into a Pod, but projection is not the same as secure storage, immediate reload, or authorization. The application and platform must agree on how values are sourced, refreshed, validated, and retired.

The central question is not “ConfigMap or Secret?” It is:

> Which authority owns this value, how is it represented in the API, how does it enter the process, when does it change, and what does the process do when it changes?

## ConfigMaps and Secrets are API objects

A ConfigMap stores non-confidential key/value or file-like data. A Secret stores values that require more restrictive handling. Secret data is base64-encoded in the API representation; base64 is not encryption. Protection depends on API authorization, etcd encryption configuration, audit/log discipline, transport security, node projection, and application behavior. Course 8 addresses those platform controls.

Course 4 uses Secret objects only as placeholders and projection contracts. It never commits a real credential value.

## Four delivery forms have different update semantics

Runtime data can enter a container through:

- environment variables;
- command/argument expansion;
- mounted ConfigMap or Secret volumes;
- projected volumes that combine several sources.

Environment values are captured when the container starts. Updating the source object does not change the process environment. A rollout or application-specific reload mechanism is required.

Mounted ConfigMap/Secret volumes are refreshed eventually by kubelet. The update is not instantaneous and the application may keep a previously opened file descriptor or cache. Mounting a key through `subPath` prevents the normal projected update from appearing in that file. Treat these details as part of the configuration contract.

## Immutable configuration reduces hidden mutation

ConfigMaps and Secrets can be declared immutable. An immutable object cannot be modified; a new name or version is needed. This simplifies caching and makes release identity clearer, at the cost of object lifecycle and rollout work.

Atlas uses immutable configuration names derived from a content digest:

```text
atlas-api-config-7c9e...
atlas-worker-config-42ab...
```

The Deployment template references the exact name, so a configuration release creates a new Pod template revision. The digest in the name is not security; it is stable content identity.

Course 7 will make this release flow GitOps-controlled. Course 4 teaches the object and rollout semantics.

## Reload ownership must be explicit

Three valid patterns are common:

1. **restart on change** — immutable config name changes the Pod template;
2. **watch and reload** — process watches projected files and validates/reloads atomically;
3. **sidecar or controller signal** — a separate component detects change and invokes a documented reload path.

All have failure modes. Restart can disrupt work. File watching can observe partial application-level state if multiple files are not versioned together. Sidecars add shared-fate complexity. The application contract must define all-or-nothing configuration versions and failure behavior.

Atlas uses restart-on-change for primary configuration in Course 4. Secret rotation remains a Course 8 concern, but the workload contract allows overlapping secret versions so a later rotation can avoid abrupt invalidation.

## Downward API exposes object context

The Downward API can project selected Pod fields and resource requests/limits into environment variables or files. Useful examples include:

- Pod name and namespace;
- Pod UID;
- labels and annotations;
- node name;
- container CPU/memory requests and limits.

This is runtime context, not a trusted authorization source. An application may use Pod UID for logging correlation, but a remote service should authenticate the workload through a real identity mechanism, not a self-reported environment variable.

## ServiceAccounts identify Kubernetes API clients

A Pod runs under a ServiceAccount. The ServiceAccount does not automatically grant useful permissions; RBAC bindings do. Nevertheless, a default token mount can expose unnecessary cluster credentials.

Atlas uses separate ServiceAccounts:

```text
atlas-api
atlas-worker
atlas-controller
atlas-maintenance
```

and sets:

```yaml
automountServiceAccountToken: false
```

unless a container genuinely needs the Kubernetes API. The Atlas API and worker do not. The custom controller does and receives a projected token with bounded audience and expiration.

## Bound projected tokens

Modern service-account token projection supports short-lived tokens with an intended audience and automatic rotation. A receiving service should validate issuer, signature, audience, expiry, and subject. A token intended for the Kubernetes API should not be accepted by a cloud service merely because both understand JWT.

The course projects the controller token explicitly:

```yaml
projected:
  sources:
  - serviceAccountToken:
      path: token
      audience: kubernetes.default.svc
      expirationSeconds: 3600
```

In-cluster clients usually also use the mounted CA and namespace. The controller must reopen or otherwise observe token rotation; caching one token forever defeats the short lifetime.

Cloud workload identity is a separate integration. Course 2 requires short-lived workload identity; Course 8 will bind ServiceAccounts to cloud principals. Course 4 records the requirement but does not pretend a local ServiceAccount is a cloud identity.

## Image pull credentials are not application credentials

An `imagePullSecret` authorizes the kubelet/container runtime to retrieve an image. It should not be mounted into the application container. Registry access, workload runtime identity, database credentials, and Kubernetes API identity are different authorities.

Course 3's supply-chain subject remains the digest. Course 8 will enforce trusted-source policy. Course 4 verifies that image retrieval configuration does not leak into application runtime data.

## Projected volumes combine sources—but do not create transactions

A projected volume can combine ConfigMaps, Secrets, Downward API, and service-account tokens into one directory. Kubelet updates the projected view, but the application should not assume a multi-file business transaction unless it uses a version marker or atomic directory-switch protocol.

Atlas configuration contains `config-version` and validates the entire directory before adopting it. A failed validation retains the previous in-memory configuration and reports a degraded condition without exposing secret content.

## Environment-variable expansion has sharp edges

Container command and args can refer to environment variables using Kubernetes expansion syntax. Missing values and shell interpretation can produce surprising behavior. Atlas images contain fixed entrypoints and receive simple flags. They do not invoke a shell to interpolate arbitrary secret text.

## Secret values must not enter diagnostic evidence

Manifests, events, logs, annotations, environment dumps, and support bundles can expose projected values. Course 4 evidence records object names, key names, resource versions, mount paths, and reload outcomes—not secret bytes.

Even Secret object YAML may contain reversible base64. Diagnostic instructions use redacted metadata queries rather than `kubectl get secret -o yaml` in shared logs.

## Configuration checksums and their limits

A common pattern annotates the Pod template with a checksum of configuration content to force rollout. The checksum must be computed from canonical relevant content and owned by the release workflow. It must not include secret values in visible annotations. A checksum change proves different input bytes; it does not prove the process adopted or validated them.

Atlas uses immutable config object names instead of a secret-value checksum. The Pod template records a non-secret configuration release ID.

## Worked failure: rotated Secret, stale process

A Secret-backed file changes. Kubelet eventually projects the new bytes, but Atlas opened the file once during startup and never reads it again. Operators see the Secret resource version change and assume rotation completed.

The missing transition is application adoption. Evidence needs:

- source Secret identity/version;
- projected-file version or hash without exposing content;
- process reload event and accepted version;
- old/new credential overlap window;
- authentication results against the dependent service.

Kubernetes fulfilled projection. The application failed its reload contract.

## Worked failure: subPath freezes a value

A single Secret key is mounted using `subPath`. The Secret changes, but the file inside the container does not. Restarting the Pod makes the new value appear. The behavior is expected: subPath mounts do not receive projected updates. The design must either restart intentionally or mount the directory and manage reload.

## Atlas configuration and identity contract

The course creates:

- immutable API and worker ConfigMaps;
- secret templates with names/keys only;
- separate ServiceAccounts;
- explicit token automount policy;
- controller projected token;
- Downward API fields for Pod identity and resource context;
- release annotations that contain no secret values;
- reload decision records.

## Capstone increment

`atlas_kube/projection.py` models environment snapshots, eventually refreshed volume projections, immutable objects, subPath behavior, token expiry/audience, and application adoption. The lab rotates values and proves that source update, projection, and application reload are three different events.

## Further reading

- ConfigMaps: <https://kubernetes.io/docs/concepts/configuration/configmap/>
- Secrets: <https://kubernetes.io/docs/concepts/configuration/secret/>
- Projected volumes: <https://kubernetes.io/docs/concepts/storage/projected-volumes/>
- Service accounts: <https://kubernetes.io/docs/concepts/security/service-accounts/>
- Downward API: <https://kubernetes.io/docs/concepts/workloads/pods/downward-api/>

## Transition

Configuration and identity make a Pod executable. Module 7 asks whether the Pod can be placed at all and how requests, limits, topology, taints, affinity, priority, and resource pressure shape that decision.

## Worked investigation — configuration changed, behavior did not

An operator updates `atlas-config` and confirms the ConfigMap contains a new worker poll interval. Existing Pods continue using the old value. The update path determines whether this is a defect.

If the value entered through an environment variable, the container received a snapshot at process creation. Kubernetes does not rewrite the environment of a running process. Pod replacement is required.

If the value entered through a projected volume, kubelet can refresh files eventually. The application must still reread the file; a process that loaded configuration once at startup will continue using the old in-memory value. A `subPath` mount also does not receive normal projected updates.

The rollout contract must therefore state both projection and consumption semantics:

| Configuration class | Projection | Application consumption | Change action |
|---|---|---|---|
| immutable release setting | env or immutable ConfigMap | startup only | new Pod template |
| dynamic bounded tuning | projected file | watched/reloaded | wait for projection and verify reload |
| secret credential | external/projected source | provider-specific reload | overlap and rotation procedure |
| identity token | projected short-lived token | client reloads before expiry | automatic rotation plus failure handling |

### Checksum annotations are triggers, not truth

A common pattern hashes configuration data into a Pod-template annotation. A changed hash creates a new ReplicaSet. This is useful only if the hash covers the exact effective configuration. Hashing a filename, omitting one referenced key, or serializing maps nondeterministically can create false stability or unnecessary rollouts. The hash should be reproducible and auditable.

### Service accounts are workload identity selectors

A ServiceAccount is not a secret bag. Pods receive identity material through projection, and authorization is decided separately. `automountServiceAccountToken: false` is appropriate for workloads that do not need the Kubernetes API. Workloads that do need it should receive a narrowly scoped identity and short-lived token audience.

Cloud workload identity adds another exchange boundary. The Kubernetes ServiceAccount, projected token, cloud trust policy, and cloud role must agree. A network path to a cloud endpoint does not grant authority, and possession of a token with the wrong audience should not either.

## Common false conclusions

- **“ConfigMap updated means application updated.”** Projection and consumption are separate transitions.
- **“Base64 makes a Secret encrypted.”** It is encoding; protection depends on transport, storage encryption, RBAC, and handling.
- **“Putting a secret in an environment variable is always safe because it is not in the image.”** It can leak through process inspection, diagnostics, or child processes.
- **“Every Pod needs a service-account token.”** Default token projection expands authority unnecessarily.
- **“Restarting all Pods rotates a credential safely.”** Rotation may require overlap and external revocation ordering.
