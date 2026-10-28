export type Plan = 'starter' | 'team' | 'enterprise';

export function isPlan(value: string): value is Plan {
  return value === 'starter' || value === 'team' || value === 'enterprise';
}

export function formatCents(cents: number): string {
  const whole = Math.floor(cents / 100);
  const remainder = cents % 100;
  return `$${whole}.${remainder.toString().padStart(2, '0')}`;
}
