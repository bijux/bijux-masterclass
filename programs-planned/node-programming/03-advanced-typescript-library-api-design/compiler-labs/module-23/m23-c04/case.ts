type BoxTogether<T>=[T]extends[unknown]?{readonly value:T}:never;type Result=BoxTogether<'a'|'b'>;const value:Result={value:'c'};console.log(value);
