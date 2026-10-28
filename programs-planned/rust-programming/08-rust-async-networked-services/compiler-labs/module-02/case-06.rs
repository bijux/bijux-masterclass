#![allow(dead_code)]
use std::{future::{ready, Future}, rc::Rc};
fn spawn_contract<F: Future + Send + 'static>(_: F) {}
fn main() { let state = Rc::new(1u8); spawn_contract(async move { ready(()).await; *state }); }
