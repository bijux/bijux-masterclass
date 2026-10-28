#![allow(dead_code, unused_imports, unused_variables)]
use std::io::Write; fn main() { let path = std::env::temp_dir().join("c6-case-sync"); let mut file = std::fs::File::create(&path).expect("create"); file.write_all(b"x").expect("write"); file.flush().expect("flush"); file.sync_all().expect("sync"); let _ = std::fs::remove_file(path); }
