#![allow(dead_code)]
use std::{marker::PhantomPinned, pin::Pin};
struct Operation { _pin: PhantomPinned }
fn move_out(_: Operation) {}
fn main() { let operation = Box::pin(Operation { _pin: PhantomPinned }); move_out(*operation); }
