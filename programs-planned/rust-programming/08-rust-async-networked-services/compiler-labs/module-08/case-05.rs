#![allow(dead_code)]
struct Response<B> { body: B }
fn response() -> Response<String> { Response { body: vec![1u8,2] } }
fn main() {}
