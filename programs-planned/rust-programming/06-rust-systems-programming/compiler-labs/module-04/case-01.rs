#![allow(dead_code, unused_imports, unused_variables)]
use std::process::Command; fn main() { let mut command = Command::new("echo"); command.arg("a b"); let _ = command.get_args().count(); }
