const handler: ProxyHandler<object> = { ownKeys() { return [1, 2]; } };
console.log(handler);
