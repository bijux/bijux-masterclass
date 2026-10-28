#![allow(dead_code, unused_imports, unused_variables)]
#![deny(unsafe_op_in_unsafe_fn)] unsafe fn read(pointer: *const u8) -> u8 { // SAFETY: caller guarantees one readable byte.
 unsafe { *pointer } } fn main() { let value=3_u8; // SAFETY: pointer refers to the live local value.
 assert_eq!(unsafe { read(&raw const value) },3); }
