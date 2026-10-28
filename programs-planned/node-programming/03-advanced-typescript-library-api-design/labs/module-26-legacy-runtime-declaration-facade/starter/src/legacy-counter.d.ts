export interface Counter{increment():number;value():number}
export function createCounter(initial?:number):Counter;
