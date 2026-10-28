export interface GraphNode { readonly id: string; readonly dependsOn: readonly string[]; }
export function validateReferences(nodes: readonly GraphNode[]): void {
  const ids = new Set(nodes.map(node => node.id));
  if (ids.size !== nodes.length) throw new Error('duplicate node id');
  for (const node of nodes) for (const dependency of node.dependsOn) {
    if (!ids.has(dependency)) throw new Error(`unknown dependency: ${dependency}`);
  }
}
