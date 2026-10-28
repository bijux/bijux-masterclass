# Reference — Argo CD object map

`Application` binds source, destination, project, sync policy, and inventory. `AppProject` restricts sources, destinations, and resource kinds. `ApplicationSet` generates Applications from governed inputs. Hooks and waves order resources. Sync status compares desired and live; health interprets resource status.

Automated sync, self-heal, and prune are separate decisions. Repository errors are not empty desired state.

## Extended reader notes

`AppProject` bounds source repositories, destinations, resource kinds, and delegated roles. `Application` binds one desired source to one destination and owns inventory, sync, health, and prune for the resulting resources. `ApplicationSet` generates Applications and therefore has fleet-scale authority. Repository and cluster Secrets establish connectivity and are high-value credentials. Hooks and sync waves influence operation order but do not provide transactions.

During diagnosis, start at the Application’s resolved revision and source error, then inspect generated manifests, resource tree, diff, sync result, health rules, Events, and Kubernetes managed fields. A green Application summary is an index, not the complete release evidence.

Production review should examine automated sync, self-heal, and prune independently. Project policy should prevent ordinary application inventories from owning protected data resources. Generator changes should show exact Application additions, removals, destinations, and revisions.
