interface Tenant { tenant: string }
function label(this: Tenant): string { return this.tenant; }
label.call({ name: 'wrong' });
