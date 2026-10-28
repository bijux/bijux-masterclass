async function* values(){yield 1;}for await(const value of values()){const n:number=value;void n;}export {};
