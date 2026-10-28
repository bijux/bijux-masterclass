const version: string = process.version;
const major = Number(version.slice(1).split('.')[0]);
if (!Number.isSafeInteger(major)) throw new Error('invalid runtime version');
console.log(major);
