import assert from 'node:assert/strict';
import test from 'node:test';
import { array, lazy, literal, nullable, number, object, refine, string, transform, tuple, union } from '../src/index.js';

test('collections preserve paths and bounded behavior', () => {
  const Row = tuple([string(), number()] as const);
  const result = array(Row, { maxLength: 3 }).safeParse([['a', 1], ['b', 'bad']]);
  assert.equal(result.ok, false);
  if (!result.ok) assert.deepEqual(result.issues[0]?.path, [1, 1]);
});

test('union, refinement, transform, and nullable compose', () => {
  const Identifier = transform(
    refine(union([string(), number()] as const), (value) => String(value).length > 0, { code: 'id.empty', message: 'empty id' }),
    (value) => String(value),
  );
  assert.equal(Identifier.parse(42), '42');
  assert.equal(nullable(Identifier).parse(null), null);
  assert.equal(literal(true).safeParse(false).ok, false);
});

test('lazy schema rejects cyclic input', () => {
  interface NodeValue { readonly value: string; readonly children: readonly NodeValue[] }
  let NodeSchema!: ReturnType<typeof lazy<NodeValue>>;
  NodeSchema = lazy<NodeValue>(() => object({ value: string(), children: array(NodeSchema) }));
  const cyclic: { value: string; children: unknown[] } = { value: 'root', children: [] };
  cyclic.children.push(cyclic);
  assert.equal(NodeSchema.safeParse(cyclic).ok, false);
});
