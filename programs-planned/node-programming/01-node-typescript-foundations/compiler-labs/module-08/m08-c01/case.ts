function portOf(value: unknown): number {
  if (typeof value !== 'object' || value === null || !('port' in value)) throw new Error('missing port');
  const port = value.port;
  if (typeof port !== 'number' || !Number.isSafeInteger(port)) throw new Error('invalid port');
  return port;
}
console.log(portOf({ port: 3000 }));
