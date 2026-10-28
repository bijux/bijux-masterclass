#![allow(dead_code)]
struct Request<B> { body: B }
fn consume<B>(request: Request<B>) -> B { request.body }
fn main() { let body = consume(Request { body: vec![1u8,2] }); assert_eq!(body.len(),2); }
