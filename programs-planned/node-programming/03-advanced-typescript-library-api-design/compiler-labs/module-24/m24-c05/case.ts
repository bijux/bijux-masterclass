type MutableRequired<T>={-readonly[K in keyof T]-?:T[K]};type Result=MutableRequired<{readonly name?:string}>;const value:Result={name:'Ada'};value.name='Grace';console.log(value);
