import http from 'node:http';

export class HttpClient {
  readonly #agent = new http.Agent({ keepAlive: true, maxSockets: 2 });
  #closed = false;

  async get(url: URL): Promise<Buffer> {
    if (this.#closed) throw new Error('client is closed');
    return await new Promise((resolve, reject) => {
      const request = http.request(url, { agent: this.#agent }, (response) => {
        const chunks: Buffer[] = [];
        response.on('data', (chunk) => chunks.push(Buffer.from(chunk)));
        response.on('end', () => resolve(Buffer.concat(chunks)));
      });
      request.on('error', reject);
      request.end();
    });
  }

  close(): void {
    this.#closed = true;
    this.#agent.destroy();
  }
}
