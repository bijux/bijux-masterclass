declare module "node:crypto" {
  export function createHash(name: string): { update(data: string | Uint8Array): any; digest(encoding?: "hex"): any };
  export function createHmac(name: string, key: Uint8Array): { update(data: string | Uint8Array): any; digest(encoding: "hex"): string };
  export function timingSafeEqual(a: Uint8Array, b: Uint8Array): boolean;
  export function randomUUID(): string;
}
declare const Buffer: {
  from(value: string | Uint8Array, encoding?: string): Uint8Array & { toString(encoding?: string): string };
};
