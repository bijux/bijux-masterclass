#![allow(dead_code, unused_imports, unused_variables)]
use std::alloc::{Layout,dealloc}; fn main(){let mut value=0_u64;dealloc((&raw mut value).cast(),Layout::new::<u64>());}
