#![allow(dead_code, unused_imports, unused_variables)]
use std::ptr::NonNull; fn main(){let mut value=5_u8;let handle=NonNull::new(&raw mut value).expect("non-null");assert_eq!(handle.as_ptr(),&raw mut value);}
