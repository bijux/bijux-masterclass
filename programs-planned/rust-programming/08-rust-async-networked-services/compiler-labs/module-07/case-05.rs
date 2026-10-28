#![allow(dead_code)]
fn main() { let token = String::from("cancel"); let future = async move { token.len() }; println!("{token}"); drop(future); }
