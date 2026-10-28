#![allow(dead_code, unused_imports, unused_variables)]
fn main(){let pointer=Box::into_raw(Box::new(9_u32)); // SAFETY: pointer came from one Box and has not been reconstructed before.
 let owner=unsafe{Box::from_raw(pointer)};assert_eq!(*owner,9);}
