#![allow(dead_code, unused_imports, unused_variables)]
use std::ptr::NonNull; fn main(){ let mut value=4_u32; let pointer=NonNull::from(&mut value); assert_eq!(pointer.as_ptr(), &raw mut value); }
