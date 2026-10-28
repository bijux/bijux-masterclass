#![allow(dead_code)]
fn call_twice<F: FnMut()>(mut f: F) { f(); f(); }
fn main() { let value = String::from("once"); call_twice(move || drop(value)); }
