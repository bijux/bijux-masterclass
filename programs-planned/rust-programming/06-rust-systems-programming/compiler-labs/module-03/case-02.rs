#![allow(dead_code, unused_imports, unused_variables)]
use std::path::{Component, Path}; fn safe(path: &Path) -> bool { path.components().all(|part| matches!(part, Component::Normal(_))) } fn main() { assert!(safe(Path::new("a/b"))); }
