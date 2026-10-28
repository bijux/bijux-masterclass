class Range implements Iterable<number> { constructor(readonly end: number) {} *[Symbol.iterator](): Iterator<number> { for (let i=0;i<this.end;i+=1) yield i; } }
console.log([...new Range(3)]);
