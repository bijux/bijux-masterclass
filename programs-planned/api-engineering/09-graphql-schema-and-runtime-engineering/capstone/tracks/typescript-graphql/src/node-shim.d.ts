declare module "node:crypto" {
  export function createHash(name: string): {
    update(data: string | Uint8Array): any;
    digest(encoding?: string): any;
  };
  export function createHmac(name: string, key: Uint8Array): {
    update(data: string | Uint8Array): any;
    digest(): Buffer;
  };
  export function timingSafeEqual(a: Uint8Array, b: Uint8Array): boolean;
}

declare class Buffer extends Uint8Array {
  static from(value: string | Uint8Array, encoding?: string): Buffer;
  static concat(values: Uint8Array[]): Buffer;
  toString(encoding?: string): string;
  subarray(start?: number, end?: number): Buffer;
}
