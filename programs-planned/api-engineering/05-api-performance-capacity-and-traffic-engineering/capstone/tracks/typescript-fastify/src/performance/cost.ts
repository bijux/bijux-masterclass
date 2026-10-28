import { compare, decimal, divide, formatDecimal } from "./decimal.js";

export function costPerUsefulCompletion(
  totalCost: string,
  usefulCompletions: string,
): { totalCost: string; usefulCompletions: string; costPerCompletion: string } {
  const cost = decimal(totalCost);
  const completions = decimal(usefulCompletions);
  if (compare(cost, decimal("0")) < 0 || compare(completions, decimal("0")) <= 0) {
    throw new Error("invalid cost inputs");
  }
  return {
    totalCost: formatDecimal(cost),
    usefulCompletions: formatDecimal(completions),
    costPerCompletion: formatDecimal(divide(cost, completions)),
  };
}
