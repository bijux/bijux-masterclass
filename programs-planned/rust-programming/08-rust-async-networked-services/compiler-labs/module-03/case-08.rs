#![allow(dead_code)]
fn invalid<'a>() -> &'a [u8] { let bytes = vec![1u8,2,3]; &bytes }
fn main() {}
