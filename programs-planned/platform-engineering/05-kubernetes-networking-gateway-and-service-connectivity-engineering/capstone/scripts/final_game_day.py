from common import emit
scenarios=[
 {'name':'route','firstFailure':'route-selection','owner':'CNI/node routing'},
 {'name':'service','firstFailure':'service-programming','owner':'service data plane'},
 {'name':'dns','firstFailure':'client-cache-freshness','owner':'application resolver'},
 {'name':'policy','firstFailure':'egress-policy','owner':'NetworkPolicy implementation'},
 {'name':'gateway','firstFailure':'route-attachment','owner':'Gateway controller'},
 {'name':'tls','firstFailure':'certificate-hostname','owner':'Gateway certificate lifecycle'},
 {'name':'egress','firstFailure':'connected-peer-policy','owner':'egress client/proxy'}]
emit('module-10-game-day.json',{'scenarios':scenarios,'cleanup':'baseline-restored'})
