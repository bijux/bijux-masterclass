const values = [1, 2, 3];
const total = values.reduce((sum: number, value) => sum + value.toString(), 0);
console.log(total);
