interface Policy { tenant: string; describe(this: Policy): string }
const base: Pick<Policy, 'describe'> = { describe() { return this.tenant; } };
const policy = Object.assign(Object.create(base) as Policy, { tenant: 'alpha' });
console.log(policy.describe());
