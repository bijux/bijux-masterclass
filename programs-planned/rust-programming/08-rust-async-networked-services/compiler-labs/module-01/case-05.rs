#![allow(dead_code)]
use std::future::Future;
fn require_static<F: Future + 'static>(_: F) {}
fn main() { let text = String::from("borrowed"); require_static(async { text.len() }); }
