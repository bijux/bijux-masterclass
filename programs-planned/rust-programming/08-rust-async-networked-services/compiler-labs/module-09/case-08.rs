#![allow(dead_code)]
use std::{future::{ready, Future}, rc::Rc};
fn require_send<F: Future + Send>(_: F) {}
fn main() { let history = Rc::new(vec![1u8]); require_send(async move { ready(()).await; history.len() }); }
