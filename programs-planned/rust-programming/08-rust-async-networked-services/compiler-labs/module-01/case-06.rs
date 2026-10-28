#![allow(dead_code)]
use std::{future::{ready, Future}, rc::Rc};
fn require_send<F: Future + Send>(_: F) {}
fn main() { let value = Rc::new(3); require_send(async move { ready(()).await; *value }); }
