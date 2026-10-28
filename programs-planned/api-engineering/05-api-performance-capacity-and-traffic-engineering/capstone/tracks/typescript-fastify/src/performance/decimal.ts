export interface DecimalValue {
  units: bigint;
  scale: number;
}

function pow10(scale: number): bigint {
  if (!Number.isSafeInteger(scale) || scale < 0 || scale > 30) {
    throw new Error("invalid decimal scale");
  }
  return 10n ** BigInt(scale);
}

export function decimal(value: string): DecimalValue {
  const match = /^([+-]?)([0-9]+)(?:\.([0-9]+))?$/.exec(value);
  if (match === null) throw new Error("invalid decimal");
  const sign = match[1] === "-" ? -1n : 1n;
  const integer = match[2] ?? "0";
  const fraction = match[3] ?? "";
  return normalize({
    units: sign * BigInt(integer + fraction),
    scale: fraction.length,
  });
}

export function normalize(value: DecimalValue): DecimalValue {
  let units = value.units;
  let scale = value.scale;
  while (scale > 0 && units % 10n === 0n) {
    units /= 10n;
    scale -= 1;
  }
  return { units, scale };
}

function align(left: DecimalValue, right: DecimalValue): [bigint, bigint, number] {
  const scale = Math.max(left.scale, right.scale);
  return [
    left.units * pow10(scale - left.scale),
    right.units * pow10(scale - right.scale),
    scale,
  ];
}

export function add(left: DecimalValue, right: DecimalValue): DecimalValue {
  const [a, b, scale] = align(left, right);
  return normalize({ units: a + b, scale });
}

export function subtract(left: DecimalValue, right: DecimalValue): DecimalValue {
  const [a, b, scale] = align(left, right);
  return normalize({ units: a - b, scale });
}

export function multiply(left: DecimalValue, right: DecimalValue): DecimalValue {
  return normalize({ units: left.units * right.units, scale: left.scale + right.scale });
}

export function divide(
  left: DecimalValue,
  right: DecimalValue,
  precision = 12,
): DecimalValue {
  if (right.units === 0n) throw new Error("division by zero");
  const shift = precision + right.scale - left.scale;
  let numerator = left.units;
  if (shift >= 0) numerator *= pow10(shift);
  else numerator /= pow10(-shift);
  const negative = (numerator < 0n) !== (right.units < 0n);
  const absNumerator = numerator < 0n ? -numerator : numerator;
  const absDenominator = right.units < 0n ? -right.units : right.units;
  const quotient = absNumerator / absDenominator;
  const remainder = absNumerator % absDenominator;
  const rounded = quotient + (remainder * 2n >= absDenominator ? 1n : 0n);
  return normalize({ units: negative ? -rounded : rounded, scale: precision });
}

export function compare(left: DecimalValue, right: DecimalValue): number {
  const [a, b] = align(left, right);
  return a < b ? -1 : a > b ? 1 : 0;
}

export function formatDecimal(value: DecimalValue): string {
  const normalized = normalize(value);
  const negative = normalized.units < 0n;
  const digits = (negative ? -normalized.units : normalized.units).toString();
  if (normalized.scale === 0) return `${negative ? "-" : ""}${digits}`;
  const padded = digits.padStart(normalized.scale + 1, "0");
  const split = padded.length - normalized.scale;
  return `${negative ? "-" : ""}${padded.slice(0, split)}.${padded.slice(split)}`;
}
