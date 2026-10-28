#![allow(dead_code)]
struct Request<B> { body: B }
fn invalid<'a>() -> Request<&'a str> { let body = String::from("temporary"); Request { body: &body } }
fn main() {}
