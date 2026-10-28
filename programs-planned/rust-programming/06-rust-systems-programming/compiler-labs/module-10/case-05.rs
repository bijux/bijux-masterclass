#![allow(dead_code, unused_imports, unused_variables)]
use std::rc::Rc; fn require_send<T:Send>(_:T){} fn main(){require_send(Rc::new(1_u8));}
