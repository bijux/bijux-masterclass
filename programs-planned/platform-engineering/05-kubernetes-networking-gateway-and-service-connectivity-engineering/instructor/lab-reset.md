# Laboratory reset

Run:

```bash
make clean
```

Then terminate any manually started fixture process. For the optional cluster lane, delete only the dedicated cluster:

```bash
kind delete cluster --name atlas-networking-lab
```

Never use broad host-firewall, route, namespace, cloud-resource, or process cleanup commands. Before and after cleanup, record the resources owned by the laboratory so that cleanup itself remains reviewable.
