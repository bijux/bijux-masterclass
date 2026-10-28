use std::rc::Rc;
#[derive(Debug)] struct Node(&'static str);
fn main(){let node=Rc::new(Node("x"));let other=Rc::clone(&node);assert!(Rc::ptr_eq(&node,&other));}
