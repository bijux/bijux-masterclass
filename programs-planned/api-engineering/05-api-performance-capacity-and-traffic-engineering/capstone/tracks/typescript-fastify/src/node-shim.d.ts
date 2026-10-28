declare module "node:crypto" {
  interface Hash {
    update(data: string | Uint8Array): Hash;
    digest(encoding: "hex"): string;
  }
  export function createHash(algorithm: "sha256"): Hash;
}

declare const process: {
  hrtime: { bigint(): bigint };
  cpuUsage(previous?: { user: number; system: number }): {
    user: number;
    system: number;
  };
};
