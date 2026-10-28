type Flags<T>={[K in keyof T]:boolean};type Result=Flags<{name:string;age:number}>;const value:Result={name:true};console.log(value);
