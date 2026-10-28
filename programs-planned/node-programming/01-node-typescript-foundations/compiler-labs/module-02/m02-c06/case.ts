const labels: string[] = ['node'];
const first = labels[0];
if (first === undefined) throw new Error('missing label');
console.log(first.toUpperCase());
