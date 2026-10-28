export type ConnectionState = 'open' | 'read-ended' | 'write-ended' | 'closed';
export const canWrite = (state: ConnectionState): boolean => state === 'open' || state === 'read-ended';
