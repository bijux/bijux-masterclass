const bytes = Buffer.alloc(4);
export const length: string = bytes.readUInt32BE(0);
