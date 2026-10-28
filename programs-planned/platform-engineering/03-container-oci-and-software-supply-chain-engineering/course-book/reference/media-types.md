# Media types and descriptor roles

Media type tells a consumer how verified bytes should be interpreted. A registry may store many manifest and blob formats; clients and policy must reject unexpected substitutions.

| Object | Typical OCI media type | Role |
|---|---|---|
| Image index | `application/vnd.oci.image.index.v1+json` | Selects manifests, often by platform |
| Image manifest | `application/vnd.oci.image.manifest.v1+json` | References one config and ordered layers |
| Image config | `application/vnd.oci.image.config.v1+json` | DiffIDs, history, process defaults, platform claims |
| Tar layer | `application/vnd.oci.image.layer.v1.tar` | Uncompressed filesystem changeset |
| Gzip layer | `application/vnd.oci.image.layer.v1.tar+gzip` | Gzip-compressed changeset |
| Artifact manifest | `application/vnd.oci.artifact.manifest.v1+json` or profile-specific manifest | Binds typed evidence to a subject |
| CycloneDX JSON | `application/vnd.cyclonedx+json` | SBOM payload profile |
| DSSE envelope | `application/vnd.dsse.envelope.v1+json` | Signed statement envelope |

Always use the profile actually emitted by the tool/spec version; do not infer semantics solely from a filename or annotation. Verification should compare expected media type, HTTP `Content-Type`, descriptor media type, and payload structure. Content negotiation must not silently downgrade an index to a format that loses subject/platform/evidence semantics.
