class Sequence { static #next = 1; static allocate(): number { return this.#next++; } }
console.log(Sequence.allocate());
