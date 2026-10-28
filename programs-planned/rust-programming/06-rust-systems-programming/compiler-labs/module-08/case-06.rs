#![allow(dead_code, unused_imports, unused_variables)]
unsafe extern "C"{fn strlen(value:*const std::ffi::c_char)->usize;} fn main(){let _=strlen(std::ptr::null());}
