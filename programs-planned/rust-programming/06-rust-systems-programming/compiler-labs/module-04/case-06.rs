#![allow(dead_code, unused_imports, unused_variables)]
use std::process::Command; fn main() { let mut child = Command::new("echo").spawn().unwrap(); let _ = child.wait_with_output().unwrap(); let _ = child.kill(); }
