use std::rc::Rc;
fn main(){let value=Rc::new(String::from("x"));let _owned=*value;}
