export interface Accounting {
    readonly inspected: number;
    readonly emitted: number;
    readonly filtered: number;
    readonly rejected: number;
}
export function assertConservation(a: Accounting): void { if (a.emitted + a.filtered + a.rejected !== a.inspected)
    throw new Error('accounting mismatch'); }
