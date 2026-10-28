#![allow(dead_code, unused_imports, unused_variables)]
use std::ffi::CStr; fn main(){let text=CStr::from_bytes_with_nul(b"frame\0").expect("valid C string");assert_eq!(text.to_bytes(),b"frame");}
