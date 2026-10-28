// Predict before compiling.
use std::fs;
fn load(path: &str) -> String { fs::read_to_string(path).unwrap_or_default() }
fn main() { assert_eq!(load("definitely-missing"), ""); }
