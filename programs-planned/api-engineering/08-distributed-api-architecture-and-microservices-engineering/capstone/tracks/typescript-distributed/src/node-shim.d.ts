declare module "node:crypto" {
  export interface Hmac {
    update(data: string | Uint8Array): Hmac;
    digest(encoding: "hex"): string;
  }
  export interface Hash {
    update(data: string | Uint8Array): Hash;
    digest(encoding: "hex"): string;
  }
  export function createHmac(name: string, key: string | Uint8Array): Hmac;
  export function createHash(name: string): Hash;
  export function timingSafeEqual(a: Uint8Array, b: Uint8Array): boolean;
}
