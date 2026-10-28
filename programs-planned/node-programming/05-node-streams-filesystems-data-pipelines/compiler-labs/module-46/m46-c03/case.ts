async function* lines(source: AsyncIterable<Uint8Array>): AsyncGenerator<string> { for await (const chunk of source) yield new TextDecoder().decode(chunk); }
void lines;
