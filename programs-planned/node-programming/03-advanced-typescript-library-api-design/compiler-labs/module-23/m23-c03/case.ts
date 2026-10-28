type Box<T>=T extends unknown?{readonly value:T}:never;type Result=Box<'a'|'b'>;const value:Result={value:'a'};console.log(value);
