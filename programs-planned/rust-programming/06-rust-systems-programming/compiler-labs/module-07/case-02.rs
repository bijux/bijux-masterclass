#![allow(dead_code, unused_imports, unused_variables)]
use std::alloc::{Layout,alloc_zeroed,dealloc}; fn main(){let layout=Layout::from_size_align(8,8).unwrap(); // SAFETY: layout is valid; allocation is checked and deallocated once with the same layout.
 unsafe{let pointer=alloc_zeroed(layout);assert!(!pointer.is_null());dealloc(pointer,layout);}}
