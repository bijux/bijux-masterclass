export type Events={readonly message:{readonly text:string}};
export class EventRouter{#listeners:Array<(value:Events['message'])=>void>=[];on(listener:(value:Events['message'])=>void){this.#listeners.push(listener);}}
