#![allow(dead_code)]
fn call_twice<F: FnMut()>(mut f: F) { f(); f(); }
fn main() { let request = String::from("one"); call_twice(move || drop(request)); }
