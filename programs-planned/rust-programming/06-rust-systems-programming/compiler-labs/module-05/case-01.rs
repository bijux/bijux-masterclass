#![allow(dead_code, unused_imports, unused_variables)]
fn main() { let value = 7_u32; let pointer = &raw const value; // SAFETY: pointer comes from a live aligned local value.
 let observed = unsafe { *pointer }; assert_eq!(observed, 7); }
