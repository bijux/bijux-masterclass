use std::rc::Rc;
#[derive(Debug)] struct Node{label:&'static str,children:Vec<Rc<Node>>}
fn main(){
 let child=Rc::new(Node{label:"c",children:vec![]});
 let old=Rc::new(Node{label:"old",children:vec![Rc::clone(&child)]});
 let new=Rc::new(Node{label:"new",children:old.children.clone()});
 assert!(Rc::ptr_eq(&old.children[0],&new.children[0]));
}
