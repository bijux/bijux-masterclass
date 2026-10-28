class Service { value = 4; execute() { return this.value; } }
const execute: () => number = new Service().execute;
console.log(execute());
