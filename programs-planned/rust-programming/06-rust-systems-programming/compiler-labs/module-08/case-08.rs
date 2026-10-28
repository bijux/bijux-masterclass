#![allow(dead_code, unused_imports, unused_variables)]
extern "C" fn callback(_:i32){} fn main(){let pointer:fn(i32)=callback;let _=pointer;}
