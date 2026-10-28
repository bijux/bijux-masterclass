const meter = {
  value: 4,
  read(): number { return this.value; },
};
console.log(meter.read());
