type AwaitedValue<T>=T extends PromiseLike<infer U>?U:T;type Result=AwaitedValue<Promise<number>>;const value:Result=2;console.log(value);
