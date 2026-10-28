#![allow(dead_code, unused_imports, unused_variables)]
fn main() { let path = std::env::temp_dir().join("c6-case-create-new"); let file = std::fs::OpenOptions::new().write(true).create_new(true).open(&path).expect("new"); drop(file); let _ = std::fs::remove_file(path); }
