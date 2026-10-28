export interface Candidate { readonly address: string; readonly family: 4 | 6 }
export const ipv4 = (values: readonly Candidate[]): readonly Candidate[] => values.filter((value) => value.family === 4);
