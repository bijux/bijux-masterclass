/**
 * Dependency-light ambient declarations used only by `typescript-syntax-proof`.
 *
 * They give the TypeScript compiler enough surface to check this repository's
 * own declarations, control flow, imports, and cross-file types without
 * pretending to replace the real package type definitions. `npm run typecheck`
 * remains the authoritative dependency-backed type proof.
 */

interface Buffer extends Uint8Array {
  toString(encoding?: string): string;
}
declare const Buffer: {
  from(value: string | ArrayBuffer | ArrayLike<number>, encoding?: string): Buffer;
  concat(values: readonly Uint8Array[]): Buffer;
  isBuffer(value: unknown): value is Buffer;
};

declare const process: {
  env: Record<string, string | undefined>;
  argv: string[];
  pid: number;
  exitCode?: number;
  on(signal: NodeJS.Signals | "SIGINT" | "SIGTERM", listener: () => void): void;
  once(signal: NodeJS.Signals | "SIGINT" | "SIGTERM", listener: () => void): void;
};

declare namespace NodeJS {
  interface ErrnoException extends Error { code?: string }
  type Signals = "SIGINT" | "SIGTERM" | "SIGHUP" | "SIGQUIT";
}

declare module "node:crypto" {
  export function randomUUID(): string;
  export function randomBytes(size: number): Buffer;
  export function createHash(algorithm: string): {
    update(value: Uint8Array | string, encoding?: string): any;
    digest(encoding: "hex"): string;
  };
  export function createHmac(algorithm: string, key: string | Uint8Array): {
    update(value: Uint8Array | string, encoding?: string): any;
    digest(encoding: "hex"): string;
    digest(): Buffer;
  };
  export function timingSafeEqual(left: Uint8Array, right: Uint8Array): boolean;
}

declare module "node:fs" {
  import type { Readable, Writable } from "node:stream";
  export function createReadStream(path: string, options?: unknown): Readable;
  export function createWriteStream(path: string, options?: unknown): Writable;
  export function mkdirSync(path: string, options?: unknown): void;
}

declare module "node:fs/promises" {
  export function link(existingPath: string, newPath: string): Promise<void>;
  export function lstat(path: string): Promise<any>;
  export function mkdir(path: string, options?: unknown): Promise<void>;
  export function mkdtemp(prefix: string): Promise<string>;
  export function open(path: string, flags?: string): Promise<any>;
  export function readFile(path: string, options?: unknown): Promise<any>;
  export function realpath(path: string): Promise<string>;
  export function readdir(path: string): Promise<string[]>;
  export function rm(path: string, options?: unknown): Promise<void>;
  export function stat(path: string): Promise<any>;
  export function writeFile(path: string, data: Uint8Array | string, options?: unknown): Promise<void>;
}

declare module "node:os" {
  export function tmpdir(): string;
}

declare module "node:path" {
  export const sep: string;
  export function dirname(path: string): string;
  export function isAbsolute(path: string): boolean;
  export function join(...parts: string[]): string;
  export function relative(from: string, to: string): string;
  export function resolve(...parts: string[]): string;
}

declare module "node:stream" {
  export class Readable implements AsyncIterable<Uint8Array> {
    static from(values: Iterable<unknown> | AsyncIterable<unknown>): Readable;
    [Symbol.asyncIterator](): AsyncIterator<Uint8Array>;
  }
  export class Writable {}
  export class Transform extends Readable {
    constructor(options?: {
      transform?: (
        chunk: Buffer,
        encoding: string,
        callback: (error?: Error | null, value?: unknown) => void,
      ) => void;
    });
  }
}

declare module "node:stream/promises" {
  export function pipeline(...streams: unknown[]): Promise<void>;
}

declare module "node:timers/promises" {
  export function setTimeout(milliseconds: number): Promise<void>;
}

declare module "node:url" {
  export function pathToFileURL(path: string): { href: string };
  export const URL: typeof globalThis.URL;
}

declare module "pg" {
  export interface QueryResultRow { [column: string]: any }
  export interface QueryResult<R extends QueryResultRow = QueryResultRow> {
    rows: R[];
    rowCount: number | null;
  }
  export interface PoolClient {
    query<R extends QueryResultRow = QueryResultRow>(
      text: string,
      values?: readonly unknown[],
    ): Promise<QueryResult<R>>;
    release(): void;
  }
  export class Pool {
    constructor(config?: unknown);
    connect(): Promise<PoolClient>;
    query<R extends QueryResultRow = QueryResultRow>(
      text: string,
      values?: readonly unknown[],
    ): Promise<QueryResult<R>>;
    end(): Promise<void>;
  }
  export class Client {
    constructor(config?: unknown);
    connect(): Promise<void>;
    query<R extends QueryResultRow = QueryResultRow>(
      text: string,
      values?: readonly unknown[],
    ): Promise<QueryResult<R>>;
    end(): Promise<void>;
  }
  const pg: { Pool: typeof Pool; Client: typeof Client };
  export default pg;
}

declare module "fastify" {
  export interface FastifyRequest {
    raw: any;
    headers: Record<string, string | string[] | undefined>;
    id: string;
    method: string;
    url: string;
    body: any;
    params: any;
    query: any;
    ip: string;
    log: { error(...args: any[]): void };
    file(): Promise<any>;
  }
  export interface FastifyReply {
    raw: any;
    code(status: number): FastifyReply;
    type(mediaType: string): FastifyReply;
    header(name: string, value: string | number): FastifyReply;
    hijack(): void;
    send(payload?: any): any;
  }
  export interface FastifyError extends Error {
    validation?: any[];
    statusCode?: number;
    code?: string;
  }
  export type preHandlerHookHandler = (
    request: FastifyRequest,
    reply: FastifyReply,
  ) => any;
  export interface FastifyInstance {
    log: { info(...args: any[]): void };
    register(plugin: any, options?: any): Promise<any>;
    decorate(name: string, value: any): FastifyInstance;
    addHook(name: string, handler: (...args: any[]) => any): FastifyInstance;
    addContentTypeParser(mediaType: string, options: any, parser: (...args: any[]) => any): FastifyInstance;
    setErrorHandler(
      handler: (
        error: FastifyError,
        request: FastifyRequest,
        reply: FastifyReply,
      ) => any,
    ): FastifyInstance;
    setNotFoundHandler(
      handler: (request: FastifyRequest, reply: FastifyReply) => any,
    ): FastifyInstance;
    get(
      path: string,
      options: any,
      handler: (request: FastifyRequest, reply: FastifyReply) => any,
    ): FastifyInstance;
    post(
      path: string,
      options: any,
      handler: (request: FastifyRequest, reply: FastifyReply) => any,
    ): FastifyInstance;
    patch(
      path: string,
      options: any,
      handler: (request: FastifyRequest, reply: FastifyReply) => any,
    ): FastifyInstance;
    delete(
      path: string,
      options: any,
      handler: (request: FastifyRequest, reply: FastifyReply) => any,
    ): FastifyInstance;
    listen(options: unknown): Promise<unknown>;
    close(): Promise<void>;
  }
  const Fastify: (options?: any) => FastifyInstance;
  export default Fastify;
}

declare module "@fastify/multipart" {
  import type { Readable } from "node:stream";
  export interface MultipartFile {
    mimetype: string;
    filename: string;
    file: Readable;
  }
  const plugin: any;
  export default plugin;
}

declare module "@fastify/swagger" {
  const plugin: any;
  export default plugin;
}

declare module "@fastify/swagger-ui" {
  const plugin: any;
  export default plugin;
}

declare module "@sinclair/typebox" {
  export interface TSchema { readonly [key: string]: any }
  export const Type: any;
}

declare module "vitest" {
  export const describe: any;
  export const expect: any;
  export const it: any;
}

declare module "node:crypto" {
  export function createPublicKey(options: { key: unknown; format: "jwk" }): unknown;
  export function createVerify(algorithm: string): {
    update(value: Uint8Array | string, encoding?: string): any;
    end(): any;
    verify(key: unknown, signature: Uint8Array): boolean;
  };
}


declare module "@opentelemetry/sdk-node" {
  export class NodeSDK {
    constructor(options?: unknown);
    start(): Promise<void>;
    shutdown(): Promise<void>;
  }
}

declare module "@opentelemetry/exporter-trace-otlp-http" {
  export class OTLPTraceExporter {
    constructor(options?: unknown);
  }
}
