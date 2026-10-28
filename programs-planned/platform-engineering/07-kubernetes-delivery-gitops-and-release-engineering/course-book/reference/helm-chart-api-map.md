# Reference — Helm chart API map

Chart consumers depend on chart name/version, values names and types, defaults, rendered resource identity, CRD ownership, hooks, dependencies, and upgrade behavior. `values.schema.json` governs structural inputs. Chart digest identifies package bytes. Render digest identifies output for one values set and renderer.

Argo CD renderer-only use and Flux HelmRelease use different lifecycle semantics; record the integration mode in release evidence.

## Extended reader notes

A chart exposes several coupled APIs. The **values API** defines names, types, defaults, required fields, and deprecation. The **resource identity API** determines which Kubernetes objects retain identity across upgrades. The **selector API** must remain compatible because immutable selectors can force replacement. The **hook API** defines side effects and replay behavior. The **ownership API** determines which resources Helm adopts, retains, or removes. The **operational API** includes probes, resources, shutdown, and security defaults.

Version changes according to these surfaces, not according to template line count. Adding an optional value with a safe default is usually additive. Renaming a value or changing a default that alters authority can be breaking. Renaming a resource can orphan or replace live state. Changing a hook into a destructive migration can make rollback impossible even if the chart version increments only a patch.

A chart release record should bind the package digest, chart metadata, image digests, values schema result, predecessor upgrade test, rendered-set digest, and known retained resources.
