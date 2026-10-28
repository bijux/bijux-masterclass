use std::fmt::Display;
macro_rules! show { ($value:expr) => {{ fn need<T: Display>(v: T) -> String { v.to_string() } need($value) }}; }
fn main() { assert_eq!(show!(String::from("ok")), "ok"); }
