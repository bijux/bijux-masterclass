#![allow(dead_code, unused_imports, unused_variables)]
use std::path::Path; fn sibling(path: &Path) -> std::path::PathBuf { path.parent().unwrap_or_else(|| Path::new(".")).join(".tmp") } fn main() { assert_eq!(sibling(Path::new("a/out")), Path::new("a/.tmp")); }
