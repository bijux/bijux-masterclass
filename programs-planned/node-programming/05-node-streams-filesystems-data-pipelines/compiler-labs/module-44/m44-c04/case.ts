const stream = new ReadableStream<Uint8Array>();
const reader: ReadableStreamDefaultReader<string> = stream.getReader();
void reader;
