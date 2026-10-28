#![allow(dead_code)]
#[derive(Debug, PartialEq)] enum Attempt<T> { Committed(T), Rejected, Ambiguous }
fn main() { let outcome = Attempt::Committed(3u8); assert_eq!(outcome, Attempt::Committed(3)); }
