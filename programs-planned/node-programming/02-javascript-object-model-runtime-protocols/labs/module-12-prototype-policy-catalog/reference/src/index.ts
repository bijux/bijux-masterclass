export type PolicyKey = 'maxItems' | 'retentionDays';
export interface PolicyValues { readonly maxItems: number; readonly retentionDays: number }
export interface TenantPolicy extends PolicyValues { readonly tenant: string; describe(): string }
export interface Resolution { readonly value: number; readonly source: 'own' | 'default' }
const KEYS = new Set<PolicyKey>(['maxItems','retentionDays']);
const FORBIDDEN = new Set(['__proto__','prototype','constructor']);

export function validatePositiveInteger(value: unknown, name: string): number {
  if (typeof value !== 'number' || !Number.isSafeInteger(value) || value <= 0) throw new Error(`${name} must be a positive safe integer`);
  return value;
}

export function createDefaultPolicy(values: PolicyValues): Readonly<PolicyValues & { describe(this: TenantPolicy): string }> {
  return Object.freeze({
    maxItems: validatePositiveInteger(values.maxItems,'maxItems'),
    retentionDays: validatePositiveInteger(values.retentionDays,'retentionDays'),
    describe(this: TenantPolicy): string { return `${this.tenant}: max=${this.maxItems}, retention=${this.retentionDays}`; },
  });
}

export function createTenantPolicy(defaults: object, rawTenant: string, overrides: Partial<PolicyValues>): TenantPolicy {
  const tenant=rawTenant.trim(); if (tenant==='') throw new Error('tenant must not be empty');
  const value=Object.create(defaults) as Record<PropertyKey, unknown>;
  Object.defineProperty(value,'tenant',{value:tenant,writable:false,enumerable:true,configurable:false});
  for (const key of ['maxItems','retentionDays'] as const) {
    const candidate=overrides[key];
    if (candidate!==undefined) Object.defineProperty(value,key,{value:validatePositiveInteger(candidate,key),writable:true,enumerable:true,configurable:true});
  }
  return value as unknown as TenantPolicy;
}

export function resolvePolicy(policy: TenantPolicy, key: PolicyKey): Resolution {
  return { value: policy[key], source: Object.hasOwn(policy,key)?'own':'default' };
}

export function decodeOverrides(input: unknown): Partial<PolicyValues> {
  if (typeof input!=='object'||input===null||Array.isArray(input)) throw new Error('overrides must be an object');
  const out=Object.create(null) as Partial<Record<PolicyKey,number>>;
  for (const key of Object.keys(input)) {
    if (FORBIDDEN.has(key)||!KEYS.has(key as PolicyKey)) throw new Error(`unsupported override: ${key}`);
    const value=(input as Record<string,unknown>)[key];
    const typed=key as PolicyKey;
    out[typed]=validatePositiveInteger(value,key);
  }
  return out;
}
