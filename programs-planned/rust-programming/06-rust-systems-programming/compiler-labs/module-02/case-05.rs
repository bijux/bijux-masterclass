#![allow(dead_code, unused_imports, unused_variables)]
use std::io::Write; fn main() { let path = std::env::temp_dir().join("x"); let file = std::fs::File::create(path).unwrap(); file.write_all(b"x").unwrap(); }
