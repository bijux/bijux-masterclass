export type RetryableMethod = 'GET' | 'HEAD';
export const retryable = (method:string): method is RetryableMethod => method === 'GET' || method === 'HEAD';
