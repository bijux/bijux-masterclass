const seen = new Map([['key','job-1']]);
console.log(seen.get('key') === 'job-1' ? 'replay' : 'new');
