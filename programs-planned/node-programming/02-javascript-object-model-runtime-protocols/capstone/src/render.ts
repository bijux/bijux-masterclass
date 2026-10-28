import type { NodeView } from './types.js';
export const HELP=`ObjectAtlas\n\nCommands:\n  add <id> <folder|component|service> <label> [--parent <id>]\n  set <id> <key> <json-value>\n  delete-attribute <id> <key>\n  move <id> <new-parent|root>\n  remove <id>\n  clone <source-id> <new-root-id>\n  show <id>\n  inspect <id>\n  walk [id] [--order preorder|postorder|breadth]\n  summary\n  help\n  version`;
export const VERSION='ObjectAtlas 1.0.0';
export function renderNode(node:NodeView):string{return [`id\t${node.id}`,`kind\t${node.kind}`,`label\t${node.label}`,`parent\t${node.parentId??'root'}`,`children\t${node.children.join(',')}`,`attributes\t${JSON.stringify(node.attributes)}`].join('\n');}
export function renderWalk(nodes:readonly NodeView[]):string{return nodes.map((node,index)=>`${index+1}\t${node.id}\t${node.kind}\t${node.label}`).join('\n');}
