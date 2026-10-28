interface Box<in out T>{get():T;set(value:T):void}declare const text:Box<string>;const value:Box<string|number>=text;console.log(value);
