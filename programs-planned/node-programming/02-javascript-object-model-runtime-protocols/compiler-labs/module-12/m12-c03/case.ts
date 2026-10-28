const input: Record<string, unknown> = Object.create({ limit: 99 }) as Record<string, unknown>;
const limit = Object.hasOwn(input, 'limit') ? input['limit'] : undefined;
console.log(limit);
