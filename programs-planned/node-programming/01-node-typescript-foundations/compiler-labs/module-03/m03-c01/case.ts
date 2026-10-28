function counter(): () => number {
  let value = 0;
  return () => { value += 1; return value; };
}
const next = counter();
console.log(next(), next());
