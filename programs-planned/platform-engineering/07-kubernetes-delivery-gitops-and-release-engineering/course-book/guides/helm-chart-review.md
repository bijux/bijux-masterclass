# Guide — Helm chart review

Treat a chart as a package and an operator-facing API.

Start with `Chart.yaml`, values schema, dependencies, CRD ownership, and the previous accepted chart. The chart version identifies the package; the application version is informational; image digests identify workload bytes.

Review values for type, default, meaning, and compatibility. Reject values surfaces that expose arbitrary Kubernetes fragments without a documented ownership reason. Render minimal, typical, production, and invalid combinations. Validate the complete resource set and compare it with the previous chart.

Hooks require a separate review because they execute privileged workloads and may repeat. Ask whether every hook has immutable code, least privilege, durable operation identity, timeout, retry behavior, evidence, and safe cleanup. A database change must follow the Course 6 migration protocol rather than relying on hook order alone.

When Helm is used through GitOps, identify the integration mode. Argo CD renderer-only behavior and Flux HelmRelease lifecycle do not produce identical inventories, histories, tests, or rollback behavior.

## Extended reader notes

Treat a chart release as an API review. Validate values against the schema; compare defaults with the predecessor; render minimal, default, and production values; test installation and every supported upgrade path; inspect resource identity and immutable fields; examine hooks and deletion policies; and bind the package digest.

Require immutable image digests in production values. Confirm that security context, probes, resources, shutdown, and Service selectors remain explicit. Review whether CRDs are managed separately and how their upgrades are coordinated. A chart that renders successfully but cannot upgrade from the currently installed release is not releasable.

Record retained resources and uninstall behavior. Helm ownership labels are not data-retirement evidence.
