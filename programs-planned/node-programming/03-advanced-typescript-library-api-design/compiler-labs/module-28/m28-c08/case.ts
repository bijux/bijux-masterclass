const input=JSON.parse('{"age":"old"}')as{age:number};if(!Number.isFinite(input.age))throw new Error('runtime schema was bypassed');console.log(input.age);
