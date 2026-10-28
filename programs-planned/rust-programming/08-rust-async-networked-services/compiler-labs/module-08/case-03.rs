#![allow(dead_code)]
use std::future::Future;
fn require_send<F: Future + Send>(_: F) {}
fn main() { require_send(async move { String::from("body") }); }
