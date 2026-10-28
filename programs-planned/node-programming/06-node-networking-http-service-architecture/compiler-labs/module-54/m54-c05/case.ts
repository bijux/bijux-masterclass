export interface Reply { readonly contentLength: number; readonly body: Buffer; readonly omitBody: boolean }
export const head = (body: Buffer): Reply => ({ contentLength: body.byteLength, body, omitBody: true });
