const NAME = /^[a-z][a-z0-9-]{0,62}$/;
const KIND = /^[a-z][a-z0-9-]*$/;

export function entityRef(kind: string, namespace: string, name: string): string {
  const normalizedKind = kind.trim().toLowerCase();
  if (!KIND.test(normalizedKind)) throw new Error("invalid-kind");
  if (!NAME.test(namespace) || !NAME.test(name)) throw new Error("invalid-name");
  return `${normalizedKind}:${namespace}/${name}`;
}

export function parseRef(value: string): [string, string, string] {
  const match = /^([a-z][a-z0-9-]*):([a-z][a-z0-9-]*)\/([a-z][a-z0-9-]*)$/.exec(value);
  if (!match) throw new Error("invalid-entity-ref");
  return [match[1]!, match[2]!, match[3]!];
}
