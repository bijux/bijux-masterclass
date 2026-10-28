interface Operation { (value: number): number }
const operation: Operation = (value) => value * 2;
console.log(new operation(2));
