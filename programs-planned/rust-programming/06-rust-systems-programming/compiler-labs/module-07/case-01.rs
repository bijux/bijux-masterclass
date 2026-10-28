#![allow(dead_code, unused_imports, unused_variables)]
use std::alloc::Layout; fn main(){let layout=Layout::from_size_align(64,32).expect("valid layout");assert_eq!(layout.align(),32);}
