export interface DiscoveryRequest {
  readonly nonce: string;
}

const NONCE = /^[0-9a-f]{32}$/;

export function encodeRequest(request: DiscoveryRequest): Buffer {
  if (!NONCE.test(request.nonce)) throw new Error('invalid nonce');
  return Buffer.from(`DISCOVER-V1\t${request.nonce}`, 'ascii');
}

export function decodeRequest(bytes: Uint8Array): DiscoveryRequest {
  const [tag, nonce, extra] = Buffer.from(bytes).toString('ascii').split('\t');
  if (tag !== 'DISCOVER-V1' || extra !== undefined || nonce === undefined || !NONCE.test(nonce)) {
    throw new Error('invalid request');
  }
  return { nonce };
}
