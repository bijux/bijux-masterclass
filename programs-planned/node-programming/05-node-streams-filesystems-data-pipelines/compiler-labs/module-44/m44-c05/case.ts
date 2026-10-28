async function* values(): AsyncGenerator<number, string, void> { yield 1; return 'done'; }
void values;
