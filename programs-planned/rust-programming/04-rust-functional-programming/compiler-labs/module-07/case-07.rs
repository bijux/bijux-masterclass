struct Node{value:i32,children:Vec<Node>}
fn main(){
 let root=Node{value:1,children:vec![Node{value:2,children:vec![]}]};
 let mut stack=vec![&root];let mut out=vec![];
 while let Some(node)=stack.pop(){out.push(node.value);stack.extend(node.children.iter().rev());}
 assert_eq!(out,vec![1,2]);
}
