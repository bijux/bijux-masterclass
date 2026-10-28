export const remaining = (deadline:number, now:number): number => Math.max(0, deadline-now);
