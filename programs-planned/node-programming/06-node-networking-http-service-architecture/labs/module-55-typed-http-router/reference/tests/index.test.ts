import assert from 'node:assert/strict';
import test from 'node:test';
import { Application, matchRoute, validateSubmission } from '../src/index.js';

const request = (
  method: string,
  path: string,
  body?: unknown,
  headers: readonly [string, string][] = [],
) => ({ method, url: new URL(`http://x${path}`), body, headers: new Map(headers) });

test('matches static and parameter routes precisely', () => {
  assert.deepEqual(matchRoute('GET', new URL('http://x/health')), { kind: 'health', head: false });
  assert.equal(matchRoute('GET', new URL('http://x/jobs/not-valid')).kind, 'not-found');
});

test('validates exact submissions', () => {
  assert.deepEqual(validateSubmission({ operation: 'uppercase', payload: 'x' }), {
    operation: 'uppercase', payload: 'x',
  });
  assert.throws(() => validateSubmission({ operation: 'uppercase', payload: 'x', extra: true }), /unexpected/);
});

test('replays same key and rejects same-key different request', () => {
  const app = new Application(10, 10);
  const key = 'request-key-0001';
  const first = app.dispatch(request('POST', '/jobs', { operation: 'uppercase', payload: 'hello' }, [['idempotency-key', key]]));
  const second = app.dispatch(request('POST', '/jobs', { payload: 'hello', operation: 'uppercase' }, [['idempotency-key', key]]));
  const conflict = app.dispatch(request('POST', '/jobs', { operation: 'word-count', payload: 'hello' }, [['idempotency-key', key]]));
  assert.equal(first.status, 202);
  assert.equal(second.status, 202);
  assert.deepEqual((first.body as { id: string }).id, (second.body as { id: string }).id);
  assert.equal(conflict.status, 409);
});

test('supports quoted ETags and HEAD', () => {
  const app = new Application(10, 10);
  const created = app.dispatch(request('POST', '/jobs', { operation: 'uppercase', payload: 'hello' }, [['idempotency-key', 'request-key-0001']]));
  const id = (created.body as { id: string }).id;
  const tag = created.headers.get('etag') ?? '';
  assert.equal(app.dispatch(request('GET', `/jobs/${id}`, undefined, [['if-none-match', tag]])).status, 304);
  const head = app.dispatch(request('HEAD', `/jobs/${id}`));
  assert.equal(head.status, 200);
  assert.equal(head.body, undefined);
  assert.equal(head.headers.get('etag'), tag);
});

test('rejects capacity before partial commit', () => {
  const app = new Application(1, 1);
  app.dispatch(request('POST', '/jobs', { operation: 'uppercase', payload: 'a' }, [['idempotency-key', 'request-key-0001']]));
  const result = app.dispatch(request('POST', '/jobs', { operation: 'uppercase', payload: 'b' }, [['idempotency-key', 'request-key-0002']]));
  assert.equal(result.status, 503);
});
