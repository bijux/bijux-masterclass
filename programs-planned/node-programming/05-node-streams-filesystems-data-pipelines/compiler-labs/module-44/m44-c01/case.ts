const source: AsyncIterable<Uint8Array> = { async *[Symbol.asyncIterator]() { yield new Uint8Array([1]); } };
void source;
