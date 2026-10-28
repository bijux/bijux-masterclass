#![allow(dead_code, unused_imports, unused_variables)]
fn main() { let value = u32::from_le_bytes([1, 0, 0, 0]); assert_eq!(value, 1); }
