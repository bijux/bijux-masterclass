# Command field guide

Commands are grouped by the question they answer. Exact flags vary by tool/version; preserve outputs and subjects rather than copying blindly.

## Inspect image and registry identity

```bash
docker buildx imagetools inspect REPOSITORY@sha256:...
skopeo inspect --raw docker://REPOSITORY@sha256:...
oras manifest fetch REPOSITORY@sha256:...
crane digest REPOSITORY:tag
```

Ask: what exact digest was resolved, which media type, and which platform children?

## Inspect layers and filesystems

```bash
skopeo copy docker://REPOSITORY@DIGEST oci:layout:release
umoci unpack --image layout@DIGEST bundle
find bundle/rootfs -xdev -printf '%M %u:%g %s %p\n'
tar -tvf layer.tar
```

Ask: are secrets/prohibited files present in any historical layer, not just the merged rootfs?

## Inspect runtime state

```bash
runc spec
runc create atlas
runc state atlas
runc start atlas
nsenter --target PID --mount --uts --ipc --net --pid ...
grep -E 'Uid|Gid|Cap|NoNewPrivs' /proc/PID/status
cat /proc/PID/mountinfo
```

Ask: what effective authority was applied, and did cleanup remove every resource?

## Inspect supply-chain evidence

```bash
syft REPOSITORY@DIGEST -o cyclonedx-json
cosign verify-attestation --type slsaprovenance REPOSITORY@DIGEST
cosign tree REPOSITORY@DIGEST
oras discover REPOSITORY@DIGEST
```

Ask: which subject, signer/builder/source identity, evidence profile, and policy were verified?

## Compare controlled rebuilds

```bash
skopeo inspect --raw oci:layout-a:tag | sha256sum
skopeo inspect --raw oci:layout-b:tag | sha256sum
diffoscope layout-a layout-b
```

Ask: which inputs/environment were held constant, and does equality prove only determinism or also origin trust?
