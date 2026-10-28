#![allow(dead_code, unused_imports, unused_variables)]
use std::io::{BufWriter, Write}; fn main() { let path = std::env::temp_dir().join("x"); let file = std::fs::File::create(path).unwrap(); let mut writer = BufWriter::new(file); writer.flush().unwrap(); let _file = writer.into_inner().unwrap(); writer.flush().unwrap(); }
