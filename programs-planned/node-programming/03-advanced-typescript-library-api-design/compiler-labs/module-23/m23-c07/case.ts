type Command={kind:'length';text:string}|{kind:'ping'};function run(c:Command){return c.kind==='length'?String(c.text.length):'pong';}console.log(run({kind:'length',text:'abc'}));
