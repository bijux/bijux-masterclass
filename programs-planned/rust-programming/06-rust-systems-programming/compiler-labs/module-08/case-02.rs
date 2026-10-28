#![allow(dead_code, unused_imports, unused_variables)]
#[repr(C)] struct Report{code:i32,length:usize} fn main(){assert!(std::mem::size_of::<Report>()>=std::mem::size_of::<usize>());}
