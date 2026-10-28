import { readFile } from 'node:fs/promises';
import { join } from 'node:path';

export interface TlsFixtures {
  readonly ca: Buffer;
  readonly cert: Buffer;
  readonly key: Buffer;
}

export async function loadFixtures(directory = join(process.cwd(), 'fixtures')): Promise<TlsFixtures> {
  const [ca, cert, key] = await Promise.all([
    readFile(join(directory, 'ca-cert.pem')),
    readFile(join(directory, 'server-cert.pem')),
    readFile(join(directory, 'server-key.pem')),
  ]);
  return { ca, cert, key };
}
