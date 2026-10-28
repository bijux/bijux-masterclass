#![allow(dead_code, unused_imports, unused_variables)]
#[unsafe(no_mangle)] pub extern "C" fn course6_case_symbol() -> u32 { 6 } fn main() { assert_eq!(course6_case_symbol(),6); }
