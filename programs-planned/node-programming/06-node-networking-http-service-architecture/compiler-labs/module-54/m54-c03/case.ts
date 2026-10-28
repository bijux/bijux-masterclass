export type Method = 'GET' | 'HEAD' | 'POST';
export const permitsBody = (method: Method): boolean => method === 'POST';
