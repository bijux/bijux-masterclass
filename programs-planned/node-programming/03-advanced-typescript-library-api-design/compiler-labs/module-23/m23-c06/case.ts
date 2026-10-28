type Strings<T>=T extends string?T:never;type Result=Strings<'a'|1|'b'>;const value:Result=1;console.log(value);
