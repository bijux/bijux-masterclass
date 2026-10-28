type Route = {kind:'health'} | {kind:'stats'};
export function handle(route: Route): number { switch(route.kind) { case 'health': return 200; } }
