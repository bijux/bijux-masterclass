#![allow(dead_code)]
#[derive(Debug, PartialEq)] struct Launch { program: String, arguments: Vec<String> }
fn main() { let launch = Launch { program: "worker".into(), arguments: vec!["--mode".into(), "safe".into()] }; assert_eq!(launch.arguments.len(),2); }
