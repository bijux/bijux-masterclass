interface Event { readonly sequence:number }
type Listener=(event:Event)=>void;
export const listener: Listener = (event:string) => console.log(event);
