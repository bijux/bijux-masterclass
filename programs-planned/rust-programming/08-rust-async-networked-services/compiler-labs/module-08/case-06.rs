#![allow(dead_code)]
use std::{future::{ready, Future}, rc::Rc};
fn require_send<F: Future + Send>(_: F) {}
fn main() { let state = Rc::new(String::from("local")); require_send(async move { ready(()).await; state.len() }); }
