type State={kind:'ready'}|{kind:'quiescing'}|{kind:'stopped'};
export function label(state:State):string { switch(state.kind){case 'ready':return 'ready';case 'stopped':return 'stopped';} }
