const input = Object.create({ maxItems: 99 }) as Record<string, unknown>;
if (!Object.hasOwn(input, 'maxItems')) throw new Error('inherited override rejected');
console.log(input['maxItems']);
