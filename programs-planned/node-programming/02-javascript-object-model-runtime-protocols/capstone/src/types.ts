export type NodeKind = 'folder' | 'component' | 'service';
export type JsonPrimitive = string | number | boolean | null;
export type JsonValue = JsonPrimitive | readonly JsonValue[] | { readonly [key: string]: JsonValue };
export type TraversalOrder = 'preorder' | 'postorder' | 'breadth';

export interface NodeRecord {
  readonly id: string;
  readonly kind: NodeKind;
  readonly label: string;
  readonly parentId: string | null;
  readonly children: readonly string[];
  readonly attributes: Readonly<Record<string, JsonValue>>;
}

export interface AtlasSnapshot {
  readonly format: 'OBJECT_ATLAS_V1';
  readonly revision: number;
  readonly roots: readonly string[];
  readonly nodes: readonly NodeRecord[];
}

export interface NodeView extends NodeRecord {
  readonly childCount: number;
  readonly policy: Readonly<{ readonly mayHaveChildren: boolean; readonly displayKind: string }>;
}
