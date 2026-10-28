import { Transform, type TransformCallback } from 'node:stream';
export class ByteCounter extends Transform {
    #bytes = 0;
    get bytes(): number { return this.#bytes; }
    override _transform(chunk: Buffer, _encoding: BufferEncoding, callback: TransformCallback): void { this.#bytes += chunk.length; callback(null, chunk); }
}
export interface StreamSnapshot {
    readonly readable: boolean;
    readonly writable: boolean;
    readonly destroyed: boolean;
}
export function snapshot(stream: NodeJS.ReadWriteStream & {
    readonly destroyed: boolean;
}): StreamSnapshot { return { readable: stream.readable, writable: stream.writable, destroyed: stream.destroyed }; }
