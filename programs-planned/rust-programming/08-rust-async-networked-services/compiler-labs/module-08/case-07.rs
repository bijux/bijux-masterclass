#![allow(dead_code)]
enum Method { Get, Post, Delete }
fn label(method: Method) -> &'static str { match method { Method::Get => "GET", Method::Post => "POST" } }
fn main() {}
