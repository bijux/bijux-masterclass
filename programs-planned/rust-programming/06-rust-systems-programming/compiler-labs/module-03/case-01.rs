#![allow(dead_code, unused_imports, unused_variables)]
fn main() { let mut path = std::path::PathBuf::from("root"); path.push("child"); assert!(path.ends_with("child")); }
