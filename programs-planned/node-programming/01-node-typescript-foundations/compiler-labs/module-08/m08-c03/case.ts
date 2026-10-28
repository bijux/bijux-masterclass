interface Config { readonly output: { readonly directory: string } }
const config = JSON.parse('{"output":null}') as Config;
console.log(config.output.directory.length);
