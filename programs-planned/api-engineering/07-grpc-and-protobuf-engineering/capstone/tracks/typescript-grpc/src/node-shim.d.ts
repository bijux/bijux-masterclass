declare module "node:crypto" {
  export interface Hash {
    update(data: string | Uint8Array): Hash;
    digest(encoding: "hex"): string;
  }
  export function createHash(name: string): Hash;
  export function timingSafeEqual(a: Uint8Array, b: Uint8Array): boolean;
}
declare const Buffer: {
  from(input: Uint8Array): Uint8Array;
};
