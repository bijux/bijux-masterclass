interface Counter { value: number; add(this: Counter, amount: number): number }
const counter: Counter = { value: 1, add(amount) { this.value += amount; return this.value; } };
console.log(counter.add(2));
