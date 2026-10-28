async function run(save: () => Promise<void>, report: () => void): Promise<void> {
  await save();
  report();
}
const events: string[] = [];
await run(async () => { events.push('save'); }, () => { events.push('report'); });
console.log(events.join(','));
