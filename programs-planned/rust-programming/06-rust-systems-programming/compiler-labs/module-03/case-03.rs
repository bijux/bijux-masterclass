#![allow(dead_code, unused_imports, unused_variables)]
use std::path::Path; fn main() { assert_eq!(Path::new("a.txt").file_name(), Some(std::ffi::OsStr::new("a.txt"))); }
