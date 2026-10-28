export interface LocatedLine {
    readonly number: number;
    readonly text: string;
}
export function parseJsonLine(line: LocatedLine): unknown { try {
    return JSON.parse(line.text);
}
catch (error) {
    throw new Error(`line ${line.number}: invalid JSON`, { cause: error });
} }
export function isRecord(value: unknown): value is Record<string, unknown> { return typeof value === 'object' && value !== null && !Array.isArray(value); }
