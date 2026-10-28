class Secret { #value = 1; read() { return this.#value; } }
const proxy = new Proxy(new Secret(), {});
console.log(proxy.read());
