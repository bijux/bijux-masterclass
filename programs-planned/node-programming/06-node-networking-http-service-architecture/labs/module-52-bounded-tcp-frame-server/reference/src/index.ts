import net from 'node:net';
import { once } from 'node:events';

export class FrameProtocolError extends Error {
  constructor(readonly code: 'FRAME_TOO_LARGE' | 'TRUNCATED_PREFIX' | 'TRUNCATED_PAYLOAD') {
    super(code);
    this.name = 'FrameProtocolError';
  }
}

export function encodeFrame(payload: Uint8Array): Buffer {
  const body = Buffer.from(payload);
  if (body.byteLength > 0xffff_ffff) {
    throw new RangeError('payload is too large for a 32-bit length');
  }
  const output = Buffer.allocUnsafe(4 + body.byteLength);
  output.writeUInt32BE(body.byteLength, 0);
  body.copy(output, 4);
  return output;
}

export class FrameDecoder {
  #pending = Buffer.alloc(0);
  #expected: number | undefined;

  constructor(readonly maxFrameBytes: number) {
    if (!Number.isInteger(maxFrameBytes) || maxFrameBytes < 0) {
      throw new RangeError('maxFrameBytes must be a non-negative integer');
    }
  }

  push(chunk: Uint8Array): readonly Buffer[] {
    if (chunk.byteLength > 0) {
      this.#pending = this.#pending.byteLength === 0
        ? Buffer.from(chunk)
        : Buffer.concat([this.#pending, Buffer.from(chunk)]);
    }
    const frames: Buffer[] = [];
    while (true) {
      if (this.#expected === undefined) {
        if (this.#pending.byteLength < 4) break;
        const length = this.#pending.readUInt32BE(0);
        this.#pending = Buffer.from(this.#pending.subarray(4));
        if (length > this.maxFrameBytes) {
          this.#pending = Buffer.alloc(0);
          throw new FrameProtocolError('FRAME_TOO_LARGE');
        }
        this.#expected = length;
      }

      if (this.#pending.byteLength < this.#expected) break;
      const payload = Buffer.from(this.#pending.subarray(0, this.#expected));
      this.#pending = Buffer.from(this.#pending.subarray(this.#expected));
      this.#expected = undefined;
      frames.push(payload);
    }
    return frames;
  }

  finish(): void {
    if (this.#expected !== undefined) {
      throw new FrameProtocolError('TRUNCATED_PAYLOAD');
    }
    if (this.#pending.byteLength !== 0) {
      throw new FrameProtocolError('TRUNCATED_PREFIX');
    }
  }
}

async function writeFrame(socket: net.Socket, frame: Buffer): Promise<void> {
  if (socket.destroyed) throw new Error('socket is destroyed');
  const accepted = socket.write(frame);
  if (!accepted) await once(socket, 'drain');
}

export async function startFrameServer(options: {
  readonly host?: string;
  readonly maxFrameBytes: number;
  readonly maxConnections: number;
  readonly idleMs: number;
}): Promise<{
  readonly host: string;
  readonly port: number;
  readonly activeSockets: () => number;
  close(graceMs?: number): Promise<void>;
}> {
  if (!Number.isInteger(options.maxConnections) || options.maxConnections < 1) {
    throw new RangeError('maxConnections must be positive');
  }
  const sockets = new Set<net.Socket>();
  const server = net.createServer({ allowHalfOpen: true }, (socket) => {
    if (sockets.size >= options.maxConnections) {
      socket.destroy();
      return;
    }
    sockets.add(socket);
    const decoder = new FrameDecoder(options.maxFrameBytes);
    let chain = Promise.resolve();

    socket.setTimeout(options.idleMs, () => socket.destroy(new Error('idle timeout')));
    socket.on('data', (chunk) => {
      try {
        const frames = decoder.push(Buffer.from(chunk));
        for (const frame of frames) {
          chain = chain.then(async () => {
            const text = new TextDecoder('utf-8', { fatal: true }).decode(frame);
            await writeFrame(socket, encodeFrame(Buffer.from(text.toUpperCase(), 'utf8')));
          });
        }
      } catch (error) {
        socket.destroy(error instanceof Error ? error : new Error('protocol error'));
      }
    });
    socket.on('end', () => {
      try {
        decoder.finish();
        chain.then(() => socket.end(), (error: unknown) => {
          socket.destroy(error instanceof Error ? error : new Error('write failed'));
        });
      } catch (error) {
        socket.destroy(error instanceof Error ? error : new Error('truncated input'));
      }
    });
    socket.once('close', () => sockets.delete(socket));
    socket.on('error', () => {});
  });

  await new Promise<void>((resolve, reject) => {
    server.once('error', reject);
    server.listen({ host: options.host ?? '127.0.0.1', port: 0 }, () => {
      server.off('error', reject);
      resolve();
    });
  });
  const observed = server.address();
  if (observed === null || typeof observed === 'string') {
    server.close();
    throw new Error('expected IP address');
  }

  return {
    host: observed.address,
    port: observed.port,
    activeSockets: () => sockets.size,
    close: async (graceMs = 100) => {
      await new Promise<void>((resolve) => server.close(() => resolve()));
      const deadline = Date.now() + graceMs;
      while (sockets.size > 0 && Date.now() < deadline) {
        await new Promise((resolve) => setTimeout(resolve, 5));
      }
      for (const socket of sockets) socket.destroy();
      if (sockets.size > 0) await Promise.all([...sockets].map((socket) => once(socket, 'close').then(() => undefined)));
    },
  };
}
