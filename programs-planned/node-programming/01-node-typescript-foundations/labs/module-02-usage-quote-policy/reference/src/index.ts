export type Plan = 'starter' | 'team' | 'enterprise';

export interface Quote {
  readonly plan: Plan;
  readonly units: number;
  readonly includedUnits: number;
  readonly billableUnits: number;
  readonly totalCents: number;
}

const POLICIES: Readonly<Record<Plan, { readonly included: number; readonly centsPerExtra: number }>> = {
  starter: { included: 100, centsPerExtra: 5 },
  team: { included: 1_000, centsPerExtra: 2 },
  enterprise: { included: 0, centsPerExtra: 0 },
};

export function isPlan(value: string): value is Plan {
  return value === 'starter' || value === 'team' || value === 'enterprise';
}

export function parseUnits(raw: string): number {
  if (!/^(0|[1-9]\d*)$/.test(raw)) {
    throw new Error('units must be decimal digits without whitespace or sign');
  }
  const units = Number(raw);
  if (!Number.isSafeInteger(units) || units > 1_000_000) {
    throw new Error('units are outside the supported range');
  }
  return units;
}

export function quoteUsage(rawUnits: string, rawPlan: string): Quote {
  if (!isPlan(rawPlan)) {
    throw new Error(`unsupported plan: ${rawPlan}`);
  }
  const units = parseUnits(rawUnits);
  const policy = POLICIES[rawPlan];
  const billableUnits = Math.max(0, units - policy.included);
  return {
    plan: rawPlan,
    units,
    includedUnits: policy.included,
    billableUnits,
    totalCents: billableUnits * policy.centsPerExtra,
  };
}

export function formatCents(cents: number): string {
  if (!Number.isSafeInteger(cents) || cents < 0) throw new Error('cents must be a nonnegative safe integer');
  const whole = Math.floor(cents / 100);
  const remainder = cents % 100;
  return `$${whole}.${remainder.toString().padStart(2, '0')}`;
}
