class Account { #balance = 1; read() { return this.#balance; } }
const forged = Object.setPrototypeOf({}, Account.prototype) as Account;
console.log(forged.read());
