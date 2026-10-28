#![allow(dead_code, unused_imports, unused_variables)]
fn main(){let pointer=Box::into_raw(Box::new(1_u8));let _=Box::from_raw(pointer);}
