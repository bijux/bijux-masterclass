const stream = new ReadableStream<Uint8Array>({ start(controller) { controller.enqueue(new Uint8Array([1])); controller.close(); } });
const reader: ReadableStreamDefaultReader<Uint8Array> = stream.getReader();
void reader;
