#![allow(dead_code, unused_imports, unused_variables)]
use std::alloc::{Layout,alloc}; fn main(){let layout=Layout::new::<u64>();let _=alloc(layout);}
