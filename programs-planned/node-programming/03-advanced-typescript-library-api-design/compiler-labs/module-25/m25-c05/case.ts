interface Box<in out T>{get():T;set(value:T):void}const box:Box<string>={get:()=>'',set:value=>console.log(value)};void box;
