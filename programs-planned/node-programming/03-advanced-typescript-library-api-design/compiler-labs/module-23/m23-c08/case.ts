type Command={kind:'ping'};const input=JSON.parse('{"kind":"delete"}') as Command;if(input.kind!=='ping')throw new Error('unsupported command');console.log('pong');
