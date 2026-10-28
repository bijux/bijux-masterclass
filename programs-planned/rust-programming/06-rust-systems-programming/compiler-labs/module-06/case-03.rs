#![allow(dead_code, unused_imports, unused_variables)]
use std::ptr::addr_of; #[repr(C)] struct Pair{a:u8,b:u32} fn main(){let pair=Pair{a:1,b:2};let pointer=addr_of!(pair.b);assert!(!pointer.is_null());}
