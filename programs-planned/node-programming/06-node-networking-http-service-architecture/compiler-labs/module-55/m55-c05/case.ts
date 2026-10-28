export type Code = 'INVALID_REQUEST' | 'NOT_FOUND' | 'OVER_CAPACITY';
export interface Problem { readonly code: Code; readonly status: number; readonly detail: string }
