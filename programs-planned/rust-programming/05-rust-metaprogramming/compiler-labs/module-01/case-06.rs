use std::fmt::Display;
struct NotDisplay;
macro_rules! show { ($value:expr) => {{ fn need<T: Display>(v: T) -> String { v.to_string() } need($value) }}; }
fn main() { let _ = show!(NotDisplay); }
