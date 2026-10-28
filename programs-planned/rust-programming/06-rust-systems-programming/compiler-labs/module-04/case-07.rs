#![allow(dead_code, unused_imports, unused_variables)]
use std::process::Command; fn main() { let mut command = Command::new("tool"); command.env(1_u32, 2_u32); }
