#![allow(dead_code, unused_imports, unused_variables)]
fn classify(status: &std::process::ExitStatus) -> Option<i32> { status.code() } fn main() { let _ = classify; }
