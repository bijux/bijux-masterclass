# Workload-controller choice

| Workload invariant | Controller |
|---|---|
| replaceable continuously running replicas | Deployment |
| finite completion with retry accounting | Job |
| scheduled creation of finite runs | CronJob owning Jobs |
| one eligible Pod per Node | DaemonSet |
| stable ordinal/network/storage identity | StatefulSet |
| new desired-state relationship not expressible by native APIs | custom resource and controller |

Use the smallest controller whose ownership model matches the invariant. “More powerful” is not “more correct.”
