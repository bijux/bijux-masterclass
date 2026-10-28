#![allow(dead_code)]
fn main() { let host = String::from("example.test"); let resolver = move || host.len(); println!("{host}"); let _ = resolver(); }
