export interface User{readonly name:string}
export function label(value:User):string{return value.name;}console.log(label({name:'Ada'}));
