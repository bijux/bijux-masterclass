interface Store { save(value: string): Promise<void> }
async function persist(store: Store): Promise<void> { await store.save('x'); }
void persist({ load: async () => 'x' });
