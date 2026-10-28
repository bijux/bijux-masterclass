#![allow(dead_code, unused_imports, unused_variables)]
use std::process::Command; fn main() { let mut command = Command::new("tool"); command.env_clear().env("MODE", "test"); assert_eq!(command.get_envs().count(), 1); }
