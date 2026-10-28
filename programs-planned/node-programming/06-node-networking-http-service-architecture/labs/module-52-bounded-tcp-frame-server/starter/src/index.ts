export function encodeFrame(payload: Uint8Array): Buffer {
  const body = Buffer.from(payload);
  const output = Buffer.allocUnsafe(4 + body.byteLength);
  output.writeUInt32BE(body.byteLength, 0);
  body.copy(output, 4);
  return output;
}

export class FrameDecoder {
  #pending = Buffer.alloc(0);

  push(chunk: Uint8Array): readonly Buffer[] {
    this.#pending = Buffer.concat([this.#pending, Buffer.from(chunk)]);
    const frames: Buffer[] = [];
    while (this.#pending.byteLength >= 4) {
      const length = this.#pending.readUInt32BE(0);
      if (this.#pending.byteLength < 4 + length) break;
      frames.push(Buffer.from(this.#pending.subarray(4, 4 + length)));
      this.#pending = Buffer.from(this.#pending.subarray(4 + length));
    }
    return frames;
  }
}
