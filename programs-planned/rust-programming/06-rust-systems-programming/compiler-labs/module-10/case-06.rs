#![allow(dead_code, unused_imports, unused_variables)]
fn main(){let mut value=0_u8;let borrow=&mut value;let _=std::panic::catch_unwind(||*borrow+=1);}
