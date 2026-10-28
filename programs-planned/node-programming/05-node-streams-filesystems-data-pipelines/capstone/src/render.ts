export function render(value: unknown): string {
  return `${JSON.stringify(value, null, 2)}\n`;
}

export const HELP = `FlowLedger — bounded NDJSON data pipelines

Commands:
  flowledger inspect <input> [--gzip-input]
  flowledger normalize <input> <output> [--gzip-input] [--gzip-output] [--replace]
  flowledger filter <input> <output> --kind <kind> [--gzip-input] [--gzip-output] [--replace]
  flowledger verify <input> --sha256 <hex>
  flowledger through <input> <output> [--replace] -- <program> [argument...]
  flowledger help
  flowledger version
`;
