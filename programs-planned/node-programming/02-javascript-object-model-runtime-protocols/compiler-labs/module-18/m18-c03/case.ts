const { proxy, revoke } = Proxy.revocable({ value: 1 }, {});
console.log(proxy.value); revoke();
