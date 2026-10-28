export interface ValidationIssue { readonly path: string; readonly message: string }
export function issue(path: string, message: string): ValidationIssue { return { path, message }; }
