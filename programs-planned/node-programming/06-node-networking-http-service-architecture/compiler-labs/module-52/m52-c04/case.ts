export function corrupt(frames: readonly Buffer[]): void { frames[0] = Buffer.alloc(0); }
