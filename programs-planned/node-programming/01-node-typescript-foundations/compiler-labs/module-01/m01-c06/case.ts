interface Config { readonly port: number }
const parsed = JSON.parse('{"host":"localhost"}') as Config;
console.log(parsed.port.toFixed(0));
