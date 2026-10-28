function parseText(input:unknown):string{if(typeof input!=='string')throw new Error('expected string');return input;}console.log(parseText('Ada'));
