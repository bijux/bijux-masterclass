type Event = { kind: 'message'; text: string } | { kind: 'count'; value: number };
const event = JSON.parse('{"kind":"message"}') as Event;
if (event.kind === 'message') console.log(event.text.toUpperCase());
