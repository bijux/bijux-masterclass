# Route selection and return path

For one flow record:

```text
source namespace/address
policy-routing rules
destination before translation
candidate routes
selected longest prefix
metric/next hop/interface
encapsulation endpoint
translated destination
reverse source/destination
return route
stateful firewall/NAT dependency
```

A default route does not prove the packet uses it. More-specific Pod, Service, private-endpoint, or policy routes can win. Forward success without return routing creates a timeout that resembles a destination drop.

When comparing Nodes, capture complete route and rule state at one time. A route object in a control plane is not proof of kernel programming.
