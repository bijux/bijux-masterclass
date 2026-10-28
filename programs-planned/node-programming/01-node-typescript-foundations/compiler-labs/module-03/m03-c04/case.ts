const meter = {
  value: 4,
  read(): number { return this.value; },
};
const read = meter.read;
console.log(read());
