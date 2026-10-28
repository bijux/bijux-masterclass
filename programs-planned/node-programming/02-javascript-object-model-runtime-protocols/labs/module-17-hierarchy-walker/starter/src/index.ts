export interface TreeNode { readonly id:string; readonly children:readonly string[] }
export function validateNodes(nodes:readonly TreeNode[]):Map<string,TreeNode>{const map=new Map<string,TreeNode>();for(const node of nodes){if(map.has(node.id))throw new Error(`duplicate node: ${node.id}`);map.set(node.id,Object.freeze({id:node.id,children:Object.freeze([...node.children])}));}return map;}
