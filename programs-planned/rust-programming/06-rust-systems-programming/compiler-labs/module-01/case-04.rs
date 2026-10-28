#![allow(dead_code, unused_imports, unused_variables)]
fn host_length(value: u64) -> Option<usize> { usize::try_from(value).ok() } fn main() { assert_eq!(host_length(3), Some(3)); }
