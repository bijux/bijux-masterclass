#![allow(dead_code, unused_imports, unused_variables)]
fn name(path: &std::path::Path) -> &str { path.file_name().unwrap() } fn main() {}
