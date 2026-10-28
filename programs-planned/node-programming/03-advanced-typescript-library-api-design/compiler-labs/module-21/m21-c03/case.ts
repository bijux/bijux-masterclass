const routes={health:'/health',metrics:'/metrics'} as const satisfies Record<string,`/${string}`>;const route:'/health'=routes.health;console.log(route);
