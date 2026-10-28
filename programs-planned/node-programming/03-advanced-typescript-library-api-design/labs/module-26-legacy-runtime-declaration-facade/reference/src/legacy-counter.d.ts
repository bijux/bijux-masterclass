export interface Counter{increment(step?:number):number;value():number;close():void}
export function createCounter(initial?:number):Counter;
