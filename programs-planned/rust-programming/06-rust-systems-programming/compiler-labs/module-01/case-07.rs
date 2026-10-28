#![allow(dead_code, unused_imports, unused_variables)]
fn local_bytes() -> &'static [u8] { let bytes = vec![1_u8, 2, 3]; &bytes } fn main() { let _ = local_bytes(); }
