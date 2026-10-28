export interface GraphNode { readonly id:string; readonly label:string; readonly edges:GraphNode[] }
export function createNode(id:string,label:string):GraphNode{if(id.trim()==='')throw new Error('id must not be empty');return{id:id.trim(),label,edges:[]};}
