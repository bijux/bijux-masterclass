const bytes: AsyncIterable<Uint8Array> = { async *[Symbol.asyncIterator]() { yield new Uint8Array([1]); } };
const text: AsyncIterable<string> = bytes;
void text;
