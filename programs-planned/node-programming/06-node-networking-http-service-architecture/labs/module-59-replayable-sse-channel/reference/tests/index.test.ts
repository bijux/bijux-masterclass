import assert from 'node:assert/strict';
import http from 'node:http';
import test from 'node:test';
import { EventJournal, ReplayGapError, encodeEvent, startSseServer } from '../src/index.js';

test('encodes multi-line JSON data as complete SSE fields', () => {
  const bytes = encodeEvent(1, { type: 'update', data: 'a\nb' });
  assert.match(bytes.toString(), /^id: 1\nevent: update\ndata: "a\\nb"\n\n$/);
});

test('replays retained events and detects gaps', () => {
  const journal = new EventJournal(2, 2);
  journal.append({ type: 'x', data: 1 });
  journal.append({ type: 'x', data: 2 });
  journal.append({ type: 'x', data: 3 });
  assert.throws(() => journal.open(0, () => {}), ReplayGapError);
  const opened = journal.open(1, () => {});
  assert.deepEqual(opened.replay.map((event) => event.id), [2, 3]);
  opened.dispose();
  assert.equal(journal.subscriberCount(), 0);
});

test('registers live delivery without a replay-to-live gap', () => {
  const journal = new EventJournal(8, 2);
  journal.append({ type: 'x', data: 1 });
  const live: number[] = [];
  const opened = journal.open(1, (event) => live.push(event.id));
  journal.append({ type: 'x', data: 2 });
  assert.deepEqual(opened.replay, []);
  assert.deepEqual(live, [2]);
  opened.dispose();
});

test('serves replay and cleans subscribers on client close', async () => {
  const journal = new EventJournal(8, 2);
  journal.append({ type: 'job', data: { state: 'queued' } });
  const server = await startSseServer({ journal, heartbeatMs: 20, maxSubscriberQueueBytes: 1024 });
  await new Promise<void>((resolve, reject) => {
    const request = http.get(`${server.url}?after=0`, (response) => {
      let text = '';
      response.on('data', (chunk) => {
        text += String(chunk);
        if (text.includes('event: job')) {
          request.destroy();
          resolve();
        }
      });
    });
    request.on('error', (error) => {
      if ((error as NodeJS.ErrnoException).code === 'ECONNRESET') return;
      reject(error);
    });
  });
  await new Promise((resolve) => setTimeout(resolve, 10));
  assert.equal(journal.subscriberCount(), 0);
  await server.close();
  journal.close();
});

test('rejects replay gap before opening the event stream', async () => {
  const journal = new EventJournal(1, 2);
  journal.append({ type: 'x', data: 1 });
  journal.append({ type: 'x', data: 2 });
  const server = await startSseServer({ journal, heartbeatMs: 50, maxSubscriberQueueBytes: 1024 });
  const response = await new Promise<{ status: number; type: string | undefined }>((resolve) => {
    http.get(`${server.url}?after=0`, (res) => {
      res.resume();
      res.on('end', () => resolve({ status: res.statusCode ?? 0, type: res.headers['content-type'] }));
    });
  });
  assert.equal(response.status, 409);
  assert.equal(response.type, 'application/problem+json');
  await server.close();
});
