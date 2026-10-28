#![allow(dead_code, unused_imports, unused_variables)]
fn exists(path: &std::path::Path) -> bool { let _ = std::fs::metadata(path)?; true } fn main() {}
