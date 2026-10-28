#![allow(dead_code, unused_imports, unused_variables)]
use std::io::Write; fn main() { let path = std::env::temp_dir().join("c6-case-file"); let mut file = std::fs::File::create(&path).expect("create"); file.write_all(b"x").expect("write"); let _ = std::fs::remove_file(path); }
