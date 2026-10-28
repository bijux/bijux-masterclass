export type ApplicationProtocol = 'h2' | 'http/1.1';
export const accepted = (value:string): value is ApplicationProtocol => value === 'h2' || value === 'http/1.1';
