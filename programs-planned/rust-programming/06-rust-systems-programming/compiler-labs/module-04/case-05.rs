#![allow(dead_code, unused_imports, unused_variables)]
use std::process::Command; fn main() { let text: String = Command::new("echo").output().unwrap().stdout; let _ = text; }
