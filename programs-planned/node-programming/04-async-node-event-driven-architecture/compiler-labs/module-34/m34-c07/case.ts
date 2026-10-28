import{EventEmitter}from'node:events';const e=new EventEmitter();const t=['before'];e.on('x',()=>t.push('listener'));e.emit('x');t.push('after');console.log(t.join(','));
