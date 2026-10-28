#![allow(dead_code)]
#[derive(Clone, Copy)] enum Method { Get, Post, Delete }
fn route(method: Method, path: &str) -> u16 { match (method, path) { (Method::Get, "/health") => 200, (Method::Post, "/jobs") => 202, (Method::Delete, _) => 405, _ => 404 } }
fn main() { assert_eq!(route(Method::Get, "/health"), 200); }
