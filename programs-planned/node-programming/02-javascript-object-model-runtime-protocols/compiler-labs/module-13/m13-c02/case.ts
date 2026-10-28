class Service { value = 1; execute(this: Service): number { return this.value; } }
const execute = new Service().execute;
console.log(execute());
