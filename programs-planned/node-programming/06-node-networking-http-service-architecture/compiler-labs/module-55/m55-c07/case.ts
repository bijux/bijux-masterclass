export function isName(value: unknown): value is {readonly name:string} { return typeof value === 'object' && value !== null && typeof (value as {name?:unknown}).name === 'string'; }
