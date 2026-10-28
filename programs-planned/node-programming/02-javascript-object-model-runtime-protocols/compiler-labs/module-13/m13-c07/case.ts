function join(this: { prefix: string }, left: string, right: string): string { return `${this.prefix}${left}${right}`; }
const bound = join.bind({ prefix: '>' }, 'a');
console.log(bound('b'));
