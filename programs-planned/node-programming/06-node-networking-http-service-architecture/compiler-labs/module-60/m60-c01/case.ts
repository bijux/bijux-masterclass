export type State='starting'|'ready'|'quiescing'|'draining'|'stopped';
export const accepts=(state:State):boolean=>state==='ready';
